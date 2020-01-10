#lang scheme

;; (vecinos i G)
;; Busca en el grafo G la lista de vecinos de i.
;; Retorna los vecinos del nodo i.
(define (vecinos i G)
  (if (null? G)
      #f
      (if (eqv? (caar G) i)
          (cadar G)
          (vecinos i (cdr G))
          )
      )
  )

;; (in i lista)
;; Revisa si un nodo esta en una lista de vecinos.
;; Retorna #t si es que esta el nodo en la lista y #f en caso contrario.
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
;; Compara dos caminos para retornar el mas largo.
;; Retorna el camino mas largo entre los dos.
(define (max_camino l1 l2) (if (> (car l1) (car l2)) l1 l2))

;; (nuevoVisitado node visitados)
;; Marca un nodo como visitado.
;; Retorna la lista con todos los nodos visitados hasta el momento.
(define (nuevoVisitado node visitados)
  (append (list (+ (car visitados) 1) node) (cdr visitados))
  )

;; (busqueda_completa nodo visitados grafo)
;; Revisa todos los caminos posibles desde el nodo entregado a la funcion.
;; Retorna una lista con el camino mas largo, desde el ultimo nodo visitado hasta el primero.
(define (busqueda_completa nodo visitados grafo)
  (let loop ((vec (vecinos nodo grafo)) (camino_largo visitados))
    (if (null? vec)
        camino_largo
        (let ((next (car vec)))
          (if (in next (cdr visitados))
              (loop (cdr vec) camino_largo)
              (loop (cdr vec)(max_camino
                              camino_largo
                              (busqueda_completa next (nuevoVisitado next visitados) grafo)
                              )
                    )
              )
          )
        )
    )
  )

(define (voy nodo grafo)
  (reverse (cdr (busqueda_completa nodo (append '(1) (list nodo)) grafo)))
  )