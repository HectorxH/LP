#lang scheme

;; (vecinos i G)
;; Descripcion
;; Retorno
(define (vecino i G)
  (if (null? G)
      #f
      (if (eqv? (caar G) i)
          (cadar G)
          (vecinos i (cdr G))
          )
      )
  )

;; (in i lista)
;; Descripcion
;; Retorno
(define (in i lista)
  (if (null? lista)
      #f
      (if (eqv? i (car lista))
          #t
          (in i (cdr lista))
          )
      )
  )

;; (max_camino l1 l2)
;; Descripcion
;; Retorno
(define (max_camino l1 l2) (if (> (car l1) (car l2)) l1 l2))

;; (nuevoVisitado node visitados)
;; Descripcion
;; Retorno
(define (nuevoVisitado node visitados)
  (append (list (+ (car visitados) 1) node) (cdr visitados))
  )

;; (BFS nodo visitados grafo)
;; Descripcion
;; Retorno
(define (BFS nodo visitados grafo)
  (let loop ((vec (vecinos nodo grafo)) (camino_largo visitados))
    (if (null? vec)
        camino_largo
        (let ((next (car vec)))
          (if (in next (cdr visitados))
              (loop (cdr vec) camino_largo)
              (loop (cdr vec)(max_camino
                              camino_largo
                              (BFS next (nuevoVisitado next visitados) grafo)
                              )
                    )
              )
          )
        )
    )
  )

(define (voy nodo grafo)
  (reverse (cdr (BFS nodo (append '(1) (list nodo)) grafo)))
  )