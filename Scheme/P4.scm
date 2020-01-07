#lang scheme

;; (ordenado? lista)
;; Recibe una lista y revisa si esta ordenada de menor a mayor.
;; Retorna #t si la lista esta ordenada de menor a mayor y #f si no lo esta.
(define (ordenado? lista)
  (if (null? (cdr lista))
      #t
      (if (< (car lista) (cadr lista))
          (ordenado? (cdr lista))
          #f
          )
      )
  )

;; (check_columns matriz)
;; Recibe una matriz y busca si hay una columna ordenada de menor a mayor.
;; Retorna #t si la matriz tiene una columna ordenada de menor a mayor.
(define (check_columns matriz) (ormap ordenado? matriz))

;; (check_rows matriz)
;; Recibe una matriz y busca si hay una fila ordenada de menor a mayor. 
;; Retorna #t si la matriz tiene una fila ordenada de menor a mayor.
(define check_rows
  (lambda (matriz)
    (if (null? matriz)
        #f
        (if (ordenado? (map car matriz))
            #t
            (check_columns (map cdr matriz)))
        )
    )
  )

;; (check_diagonal matriz)
;; Recibe una matriz y busca si hay una diagonal ordenada de menor a mayor.
;; Retorna #t si la matriz tiene una diagonal ordenada de menor a mayor.
(define check_diagonal
 (lambda (matriz)
    (if (null? (cdr matriz))
        #t
        (if (< (caar matriz) (cadadr matriz))
            (ordenado? (map cdr (cdr matriz)))
            #f
            )
        )
   )
  )

(define orden
  (lambda (n matriz)
    (or (check_columns matriz) (check_rows matriz) (check_diagonal matriz))
    )
  )