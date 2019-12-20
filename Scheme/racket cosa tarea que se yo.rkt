#lang scheme

(define gemelos
  (lambda (arbol1 arbol2)
    (cond
      ((and (null? arbol1) (null? arbol2)) #t)
      ((or (null? arbol1) (null? arbol2)) #f)
      (else
       (and (gemelos (cadr arbol1) (cadr arbol2)) (gemelos (caddr arbol1) (caddr arbol2)))
       )
      )
    )
  )

(define xor (lambda (x y) (not (eqv? x y))))

(define mayme
  (lambda (listadelistas min)
    (let mayme_aux ((lista listadelistas) (id1 (caar listadelistas)) (val1 (apply + (cdar listadelistas))))
      (if (null? lista) id1
          (let ((id2 (caar lista))
                (val2 (apply + (cdar lista))))
            (if (xor (> val1 val2) min)
                (mayme_aux (cdr lista) id1 val1)
                (mayme_aux (cdr lista) id2 val2)
                )
            )
          )
      )
    )
  )

(define maymecola
  (lambda (listadelistas)
    (list (mayme listadelistas #f) (mayme listadelistas #t))
    )
  )

(define vs
  (lambda (lista)
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
  )

(define ordenado?
  (lambda (lista)
    (if (null? (cdr lista))
        #t
        (if (< (car lista) (cadr lista))
            (ordenado? (cdr lista))
            #f
            )
        )
    )
  )

(define check_columns
  (lambda (matriz)
    (ormap ordenado? matriz)
    )
  )

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

(define vecinos
  (lambda (i G)
    (if (null? G)
        #f
        (if (eqv? (caar G) i)
            (cadar G)
            (vecinos i (cdr G))
            )
        )
    )
  )

(define in
  (lambda (i lista)
    (if (null? lista)
        #f
        (if (eqv? i (car lista))
            #t
            (in i (cdr lista))
            )
        )
    )
  )

(define max_camino
  (lambda (l1 l2)
    (if (> (car l1) (car l2)) l1 l2)
    )
  )


(define nuevoVisitado
  (lambda (node visitados)
    (append (list (+ (car visitados) 1) node) (cdr visitados))
    )
  )

(define BFS
  (lambda (nodo visitados grafo)
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
  )

(define voy
  (lambda (nodo grafo)
    (reverse (cdr (BFS nodo (append '(1) (list nodo)) grafo)))
    )
  )

(define unicos
  (lambda (_lista)
    (let loop ((lista (sort _lista >)) (u '()))
      (if (null? (cdr lista))
          (cons (car lista) u)
          (loop (cdr lista) (if (eqv? (car lista) (cadr lista))
                                u
                                (append (list (car lista)) u)
                                )
                )
          )
      )
    )
  )

(define armar
  (lambda (k _lista)
    (let loop ((lista (unicos _lista)) (resultado '()))
      (if (null? lista)
          (if (null? resultado) #f resultado)
          (if (member (- k (car lista)) lista)
              (loop (cdr lista) (append resultado (list (list (car lista) (- k (car lista))))))
              (loop (cdr lista) resultado)
              )
          )
      )
    )
  )

(define fpi
  (lambda (funcion umbral i)
    (let loop ((xi i) (i 0))
      (if (< (abs (- (funcion xi) xi)) umbral)
          i
          (loop (funcion xi) (+ i 1))
          )
      )
    )
  )

(define nuevaBase
  (lambda (_lista)
    (let loop ((lista _lista) (resultado '()))
      (if (null? (cdr lista))
          resultado
          (loop (cdr lista) (cons (+ (car lista) (cadr lista)) resultado))
          )
      )
    )
  )

(define cima
  (lambda (lista)
    (if (null? (cdr lista))
        (car lista)
        (cima (nuevaBase lista))
        )
    )
  )

(define segm
  (lambda (funcion lista)
      (append (filter funcion lista) (filter (negate funcion) lista))
    )
  )

(define serie
  (lambda (funcion entero)
    (let loop ((sum 0) (i 1))
      (if (> i entero) sum (loop (+ sum (funcion i)) (+ i 1)))
      )
    )
  )