#lang scheme

(define serie
  (lambda (funcion entero)
    (let loop ((sum 0) (i 1))
      (if (> i entero) sum (loop (+ sum (funcion i)) (+ i 1)))
      )
    )
  )