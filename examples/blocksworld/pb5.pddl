(define (problem pb5)
  (:domain blocksworld)
  (:objects a b c d e)
  (:init (onTable a) (onTable b) (onTable c) (onTable d) (onTable e)
    (clear a) (clear b) (clear c) (clear d) (clear e)
    (equal a a) (equal b b) (equal c c) (equal d d) (equal e e) (handempty))
  (:goal (and (on a b) (on b c) (on c d) (on d e))))