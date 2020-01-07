#lang scheme

;; (member? x lista)
;; Descripcion
;; Retorno
(define (member? x lista)
  (cond
    ((null? lista) #f)
    ((eqv? x (car lista)) #t)
    ((and (eqv? (car x) (caar lista)) (eqv? (cadr x) (cadar lista))) #t)
    ((and (eqv? (cadr x) (caar lista)) (eqv? (car x) (cadar lista))) #t)
    (else (member? x (cdr lista)))
    )
  )

;; (eliminar_duplicados _lista)
;; Descripcion
;; Retorno
(define (eliminar_duplicados _lista)
  (let loop ((lista _lista) (ans '()))
    (cond
      ((null? lista) ans)
      ((member? (car lista) (cdr lista)) (loop (cdr lista) ans))
      (else (loop (cdr lista) (cons (car lista) ans)))
      )
    )
  )

;; (armar_con_duplicados k _lista)
;; Descripcion
;; Retorno
(define (armar_con_duplicados k _lista)
  (let loop ((lista _lista) (resultado '()))
    (if (null? lista)
        (if (null? resultado) #f resultado)
        (if (member (- k (car lista)) lista)
            (loop (cdr lista) (append resultado (list (list (car lista) (- k (car lista))))))
            (loop (cdr lista) resultado)
            )
        )
    )
  )

(define (armar k lista)
  (eliminar_duplicados (armar_con_duplicados k lista))
  )