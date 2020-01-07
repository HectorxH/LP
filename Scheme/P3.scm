#lang scheme

;; (xor x y)
;; Aplica un xor logico entre sus dos parametos.
;; Retorna #t si solo uno de los parametros es verdadero y #f en caso contrario.
(define (xor x y) (not (eqv? x y)))

(define (vs lista)
  (let
      ((ope (cond
              ((eqv? (car lista) 'O) (lambda (x y) (or x y)))
              ((eqv? (car lista) 'A) (lambda (x y) (and x y)))
              ((eqv? (car lista) 'X) (lambda (x y) (xor x y)))
              )
            ))
    (let battle ((l1 (cadr lista)) (l2 (caddr lista)) (pt1 0) (pt2 0) (esPar #f))
      (if (null? l1)
          (cond
            ((> pt1 pt2) '1)
            ((< pt1 pt2) '2)
            (else #f)
            )
          (if (ope (eqv? (car l1) 1) (eqv? (car l2) 1))
              (if esPar
                  (battle (cdr l1) (cdr l2) (+ pt1 1)   pt2    #f)
                  (battle (cdr l1) (cdr l2)   pt1    (+ pt2 1) #t)
                  )
              (battle (cdr l1) (cdr l2) pt1 pt2 (not esPar))
              )
          )
      )
    )
  )