#lang scheme

(define fpi
  (lambda (funcion umbral i)
    (let loop ((xi i) (i 0))
      (if (< (abs (- (funcion xi) xi)) umbral)
          i
          (loop (funcion xi) (+ i 1))
          )
      )
    )
  )