#lang scheme

;; (member? x lista)
;; Revisa si el par x o el reverso del par x esta en lista.
;; Retorna #t si el par o su inverso estan en la lista y #f en caso contrario.
(define (member? x lista)
  (cond
    ((null? lista) #f)
    ((eqv? x (car lista)) #t)
    ((and (eqv? (car x) (caar lista)) (eqv? (cadr x) (cadar lista))) #t)
    (else (member? x (cdr lista)))
    )
  )

;; (eliminar_duplicados _lista)
;; Se encarga de eliminar los pares duplicados de la lista.
;; Retorna la lista sin los pares duplicados.
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
;; Crea la lista con los pares de numeros que cumplen con i+k=j pero con numeros duplicados.
;; Retorna la lista de pares con pares duplicados si es que hay.
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