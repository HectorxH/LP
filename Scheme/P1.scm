#lang scheme

(define (gemelos arbol1 arbol2)
  (cond
    ((and (null? arbol1) (null? arbol2)) #t)
    ((or (null? arbol1) (null? arbol2)) #f)
    (else
     (and (gemelos (cadr arbol1) (cadr arbol2)) (gemelos (caddr arbol1) (caddr arbol2)))
     )
    )
  )