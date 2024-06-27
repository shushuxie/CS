
;;有理数的表示
(defun GCD (a b)
  "最大公约数的计算"
    (if (= 0 b)
	a
	(GCD b (% a b))))

;; 
(defun make-rat (n d)
  "Create a rational number as a cons cell."
  (cons n d))
(defun make-rat (n d)
  "最简形式的分数"
  (let ((g (GCD n d)))
   (cons (/ n g) (/ d g))))

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

(setq one-half (make-rat 4 16))  ; 创建一个分数 1/2
(print-rat one-half

)










