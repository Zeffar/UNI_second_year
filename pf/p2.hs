getFromInterval :: Int -> Int -> [Int] -> [Int]
getFromInterval l r lst = do
    x <- lst
    if x >= l && x <= r
        then return x
    else []
-- getFromInterval l r lst =
--     do
--         y <- lst
--         z <- (filter(\x -> (x >= l) && (x <= r))[y])
--         return z

main = do
    print(getFromInterval 5 7 [1..10])