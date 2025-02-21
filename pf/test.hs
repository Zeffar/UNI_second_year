data Point = Pt [Int]
  deriving Show

data Arb = Empty
         | Node Int Arb Arb
  deriving Show

class ToFromArb where
  toArb   :: Point -> Arb
  fromArb :: Arb -> Point

insert :: Int -> Arb -> Arb
insert x arb = 
  case arb of
    Empty -> Node x Empty Empty
    Node y left right -> 
      if x < y
      then Node y (insert x left) right
      else Node y left (insert x right)

ltop :: [Int] -> Point
ltop x = Pt x

listfromarb :: Arb -> [Int]
listfromarb tree = 
    case tree of
        Empty -> []
        Node x left right -> listfromarb(left) ++ [x] ++ listfromarb(right)

instance ToFromArb where
  toArb (Pt coords) = 
    case coords of
        [] -> Empty
        (x:xs) -> insert x (toArb (Pt xs))

  fromArb tree      = 
    ltop (listfromarb(tree))
    

main = do
  let arbTree = toArb (Pt [1, 6, 4, 2, 8]) :: Arb
  print arbTree
  let pointList = fromArb arbTree --- :: Point
  print pointList