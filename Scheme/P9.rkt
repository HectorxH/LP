#lang scheme

(define segm
  (lambda (funcion lista)
      (append (filter funcion lista) (filter (negate funcion) lista))
    )
  )