#lang scheme

(define (segm funcion lista)
  (append (filter funcion lista) (filter (negate funcion) lista))
  )