import numpy as np, tensorflow as tf, pandas as pd

class ICLS:
    """
    Implicitly-Constrained Least Squares for Semi-Supervised Learning
    
    ICLS model for datasets that consist of both labeled and unlabeled cases.
    The logic behind the algorithm consists in assigning labels to unknown observations
    in such a way that, by doing so, the residuals in the labeled set - which are
    calculated using the coefficients determined by taking the whole data + made-up
    labels - would be smaller.
    
    Supports L2 regularization and observation weights.
    Implementation uses Tensorflow + L-BFGS.
    
    Note
    ----
    This algorithm is based on least-squares' closed-form solution, so it doesn't scale
    very well to larger datasets.
    While the algorithm can perform classification, it does so by modeling the problem as
    least-squares rather than logistic regression, which on itself can make performance lower.
    If you are performing regression rather than classification, make sure to change the ylim parameters.
    For better results, try assigning more weight to labeled observations (see fit method).
    
    Parameters
    ----------
    reg_param : float
        Regularization parameter for the L2-norm of the model coefficients.
    add_bias : bool
        Whether to add an intercept to the model.
    ylim : tuple or None
        Maximum and minimum values that the model can assign as labels to the unlabeled observations.
        Set to None for unlimited range (not recommended)
    
    Attributes
    ----------
    coef_ : array, shape (n_features,) or (n_features + 1,)
        Model coefficients. If called with 'add_bias=True', the first element corresponds to the intercept.
    yopt_ : array, shape (n_unlabeled_observations,)
        Labels assigned by the model to the unlabeled observations on which it is fit.
    
    References
    ----------
    Krijthe, J. H., & Loog, M. (2015, October). Implicitly constrained semi-supervised least squares classification.
    In International symposium on intelligent data analysis (pp. 158-169). Springer, Cham.
    
    """
    def __init__(self, reg_param=1e-3, add_bias=True, ylim=(0,1)):
        self.reg_param=reg_param
        self.add_bias=add_bias
        self.yopt_=None
        self.coef_=None
        self.ylim=ylim
        
    def fit(self, X_known, y_known, X_unknown, weights=None):
        """
        Fits an ICLS model to a dataset consisting of both labeled and unlabeled cases.
        
        Parameters
        ----------
        X_known : array or data frame, shape (n_observations, n_features):
            Features for the observations that have labels.
        y_known : array, series, or data frame, shape (n_observations,) or (n_observations, 1)
            Labels for the observations from X_known.
        X_unknown : array or data frame, shape (n_unlabeled_observations, n_features)
            Features for extra observations for which no labels are available.
        weights : None, int, float, or array
            When set to None, all observations have equal weight. When set to a number, the
            labeled observations get that number as weight while the unlabeled ones get weight=1.
            When passing an array with shape matching to X_known, sets that as case weights for
            the labeled observations and 1 for all the unlabeled ones.
            When passing an array with shape matching with X_known+X_unknown, sets that as individual
            case weights for both sets, taking the labeled ones to be the firsts.
        
        Returns
        -------
        self : returns an instance of self.
        """
        # checking inputs
        if (type(y_known)==list) or (type(y_known)==pd.core.series.Series) or (type(y_known)==pd.core.frame.DataFrame):
            y_known=np.array(y_known)
        if weights is not None:
            if (type(weights)==list) or (type(weights)==pd.core.series.Series):
                weights=np.array(weights)
            else:
                if (type(weights)!=np.ndarray) and (type(weights)!=np.matrixlib.defmatrix.matrix):
                    try:
                        (weights*weights)**weights
                        weights=np.array([weights]*X_known.shape[0])
                    except:
                        raise ValueError("'weights' must be a number, numpy array, list or pandas series")
            if weights.shape[0]==X_known.shape[0]:
                weights=np.r_[weights.reshape(-1), np.ones(X_unknown.shape[0])]
            else:
                if weights.shape[0]!=(X_known.shape[0]+X_unknown.shape[0]):
                    raise ValueError("'weights' has incorrect length")
            weights=weights.reshape(-1,1)
        assert X_known.shape[0]==y_known.shape[0]
        assert X_known.shape[1]==X_unknown.shape[1]
        if type(X_known)==pd.core.frame.DataFrame:
            X_known=np.array(X_known)
        if type(X_unknown)==pd.core.frame.DataFrame:
            X_unknown=np.array(X_unknown)
        y_known=y_known.astype('float64')
        if len(y_known.shape)>1:
            assert y_known.shape[1]==1
            
        # concatenating data
        X=np.r_[X_known, X_unknown]
        if self.add_bias:
            X=np.c_[np.ones(X.shape[0]), X]
            
        # solving linear system
        lhs_tf=tf.placeholder(tf.float32)
        rhs_tf=tf.placeholder(tf.float32)
        tf_solved=tf.matrix_solve(lhs_tf, rhs_tf)
        
        if weights is None:
            lhs=X.T.dot(X)+np.diag([self.reg_param]*X.shape[1])
        else:
            lhs=X.T.dot(X*weights)+np.diag([self.reg_param]*X.shape[1])
            
        with tf.Session() as sess:
            solved=tf_solved.eval(session=sess, feed_dict={lhs_tf:lhs, rhs_tf:X.T})
        
        # solving QP
        Xorig=tf.placeholder(tf.float32)
        Xsolved=tf.placeholder(tf.float32)
        ykn=tf.placeholder(tf.float32)
        yunk=tf.Variable(tf.random_normal([X_unknown.shape[0],1]))
        y=tf.concat([ykn,yunk], axis=0)
        w=tf.placeholder(tf.float32)
        
        if weights is not None:
            beta=tf.matmul(Xsolved,w*y)
        else:
            beta=tf.matmul(Xsolved,y)
        yhat=tf.matmul(Xorig,beta)
        loss=tf.losses.mean_squared_error(ykn, yhat[:X_known.shape[0]])
        
        optimizer = tf.contrib.opt.ScipyOptimizerInterface(loss, method='L-BFGS-B',
                                                           var_to_bounds={yunk:self.ylim})
        model = tf.global_variables_initializer()
        sess=tf.Session()
        sess.run(model)
        with sess:
            optimizer.minimize(sess, feed_dict={Xorig:X[:X_known.shape[0],:],
                                                Xsolved:solved,
                                                ykn:y_known.reshape(-1,1),
                                                w:weights})
            self.yopt_=yunk.eval(session=sess).reshape(-1)
            self.coef_=beta.eval(session=sess, feed_dict={Xorig:X[:X_known.shape[0],:],
                                                          Xsolved:solved,
                                                          ykn:y_known.reshape(-1,1),
                                                          yunk:self.yopt_.reshape(-1,1),
                                                          w:weights})
            self.coef_=self.coef_.reshape(-1)
        
        return self
    
    def predict(self, X):
        """
        Make predictions on new observations
        
        Note
        ----
        As this is a least-squares model rather than logistic, the predictions are unbounded.
        
        Parameters
        ----------
        X : array or data frame, shape (n_samples, n_features)
            Data on which to make predictions.
        
        Returns
        -------
        yhat : array, shape (n_samples,)
            Model predictions for the data.
        """
        if len(X.shape)==1:
            X=X.reshape(1,-1)
        if self.add_bias:
            X=np.c_[np.ones(X.shape[0]),X]
        pred = (X.dot(self.coef_)).reshape(-1)
        if X.shape[0]==1:
            return pred[0]
        else:
            return pred
