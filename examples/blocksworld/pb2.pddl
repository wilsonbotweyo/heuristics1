(define (problem pb2)
  (:domain blocksworld)
  (:objects a b c)
  (:init (onTable a) (onTable b) (on c b) (clear a) (clear c)
    (equal a a) (equal b b) (equal c c) (handempty))
  (:goal (and (on a b) (on b c))))