
;;有理数的表示



;; 
(defun make-rat (n d)
  "Create a rational number as a cons cell."
  (cons n d))

(defun numer (x)
  "Return the numerator of the rational number."
  (car x))

(defun denom (x)
  "Return the denominator of the rational number."
  (cdr x))

(defun print-rat (x)
  "Print the rational number."
  (newline)
  (princ (numer x))
  (princ "/")
  (princ (denom x)))

(setq one-half (make-rat 1 2))  ; 创建一个分数 1/2
(print-rat one-half
)









