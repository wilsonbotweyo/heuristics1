(define (problem pb6)
  (:domain blocksworld)
  (:objects a b c d e f)
  (:init (onTable a) (onTable b) (onTable c) (onTable d) (onTable e) (onTable f)
    (clear a) (clear b) (clear c) (clear d) (clear e) (clear f)
    (equal a a) (equal b b) (equal c c) (equal d d) (equal e e) (equal f f) (handempty))
  (:goal (and (on a b) (on b c) (on c d) (on d e) (on e f))))