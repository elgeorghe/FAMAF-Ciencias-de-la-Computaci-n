--1) a

esCero :: Int -> Bool
esCero x = x == 0

-- b 

esPositivo :: Int -> Bool
esPositivo x = x > 0

-- c 

esVocal :: Char -> Bool
esVocal a = (a == 'a') || (a == 'e') || (a == 'i') || (a == 'o') || (a == 'u')


-- 2) a

paratodo :: [Bool] -> Bool 
paratodo [] = True
paratodo (x:xs) = x && paratodo(xs)

-- b 

sumatoria :: [Int] -> Int
sumatoria [] = 0
sumatoria (x:xs) = x + sumatoria(xs)

-- c 

productoria :: [Int] -> Int
productoria [] = 1
productoria (x:xs) = x * productoria(xs)

-- d

factorial :: Int -> Int
factorial 0 = 1
factorial x = x * factorial(x-1)

-- e 

promedio :: [Int] -> Int
promedio(xs) = div(sumatoria(xs)) (length(xs))

-- 3 

pertenece :: Int -> [Int] -> Bool
pertenece x [] = False
pertenece x (y:xs) = (x == y) || pertenece x (xs)

-- 4 a

paratodo' :: [a] -> (a -> Bool) -> Bool
paratodo' [] t = True
paratodo' (x:xs) t = t(x) && paratodo' xs t

-- b 

existe' :: [a] -> (a -> Bool) -> Bool
existe' [] t = False
existe' (x:xs) t = t(x) || existe' xs t 

-- c 

sumatoria' :: [a] -> (a -> Int) -> Int
sumatoria' [] t = 0
sumatoria' (x:xs) t = t(x) + sumatoria' xs t 
  
-- d 

productoria' :: [a] -> (a -> Int) -> Int
productoria' [] t = 1
productoria' (x:xs) t = t(x) * productoria' xs t 

-- 5

paratodo2 :: [a] -> (a -> Bool) -> Bool
paratodo2 xs t = paratodo' xs t 

-- 6 a 

todosPares :: [Int] -> Bool 
todosPares (x:xs) = paratodo' (x:xs) (even) 

-- b 

premul :: Int -> Int -> Bool
premul x s = mod s x == 0


hayMultiplo :: Int -> [Int] -> Bool
hayMultiplo x (s:xs) = existe' (s:xs) (premul x)

-- c 

sumaCuadrados :: Int -> Int
sumaCuadrados n = sumatoria'[0..(n-1)] (^2)

-- d 

factorial' :: Int -> Int
factorial' n = productoria[1..n] 


-- e 
pares :: Int -> Int
pares x | (mod x 2 == 0) = x 
        | otherwise = 1


multiplicaPares :: [Int] -> Int
multiplicaPares (x:xs) = productoria' (x:xs) (pares)

-- 7 

{-- 
	*Funcion Map: A esta funcion se le da una lista y una funcion y se encarga de devolver otra  lista con cada elemento de la lista original luego de evaluar en dicha funcion.
    *Funcion Filter: Es similar a la Map pero a difierencia de dar una lista y una funcion se le da una lista y un predicado, la cual luego devuelve una nueva lista solo con los elementos que cumple ese predicado.
    *La expresion succ aqui esta definida como el siguiente numero, por eso, cuando se usa map succ lo que hace es expresar el siguiente numero.
entoces la expresion map succ [1,-4,6,2,-8] es equivalente a la lista [2, -3, 7, 3, -7]
    *La expresion Filter esPositivo filtraria los numeros que son positivos, por eso en la lista [1, -4, 6, 2, -8] quedaria [1, 6, 2] 
--}

--8 A

dup :: [Int] -> [Int]
dup [] = []
dup (x:xs) = 2*x : dup xs

-- b 

dup' :: [Int] -> [Int]
dup' xs = map (2*) (xs) 

-- 9 a 

elempar :: [Int] -> [Int]
elempar [] = []
elempar (x:xs) | (mod x 2 == 0) = x : elempar xs
               | otherwise = elempar xs 

-- b 

elempar' :: [Int] -> [Int]
elempar' xs = filter (even) (xs)

-- c
-- no encuentro forma de mejorarla

--10 a 
primIgualesA :: (Eq a) => a -> [a] -> [a]
primIgualesA a [] =  []
primIgualesA a (x:xs)   | a == x = x:(primIgualesA a xs)
                        | otherwise = []
                        
--b
primIgualesA' :: (Eq a) => a -> [a] -> [a]
primIgualesA' a (x:xs) = takeWhile (a == ) (x:xs)

--11 a

primIguales :: (Eq a) => [a] -> [a]
primIguales [] =  []
primIguales (x:y:xs)    | x == y = x : primIguales (y:xs)
                        | otherwise = [x]

--b
primIguales' :: (Eq a) => [a] -> [a]
primIguales' [] = []
primIguales' (x:xs) = primIgualesA' (x) (x:xs)

--12 a
cuantGen :: (b -> b -> b) -> b -> [a] -> (a -> b) -> b
cuantGen op z [] t = z
cuantGen op z (x:xs) t = t(x) `op` (cuantGen op z xs t)

--b
paratodo''' xs t = cuantGen (&&) (True) xs t

existe''' xs t = cuantGen (||) (False) xs t

sumatoria''' xs t = cuantGen (+) (0) xs t

productoria'''  xs t = cuantGen (*) (1) xs t

--13 
{--
	a) f :: (a, b) -> ...
		f (x , y) = ...
		El tipo de f es tuplas de 2 elementos. Este esta bien, porque si se quiere  trabajar con tuplas ahi estamos trabajando con cada elemento particular de las tuplas
	b) f :: [(a, b)] -> ...
		f (a , b) = ...
		El tipo de f es lista de tuplas de 2 elementos. Este esta mal ya que no esta bien definida la lista, lo que se deberia hacer es: ((a, b):xs) asi seria una lista y podemos acceder a todos los elementos de las tuplas
	c) f :: [(a, b)] -> ...
		f (x:xs) = ...
		El tipo de f es lista de tuplas de 2 elementos. Este caso esta mal debido a que no se puede acceder a cada elemento de la tupla, se deberia de poner: ((a, b):xs)
    
	d) f :: [(a, b)] -> ...
		f ((x, y) : ((a, b) : xs)) = ...
		El tipo de f es lista de tuplas de 2 elementos. Este esta bien definido.
    
	e) f :: [(Int, a)] -> ...
		f [(0, a)] = ...
		El tipo de f es lista de tuplas de 2 elementos. Pero esta mal tipado ya que no se puede hacer recursion en xs.
    
	f)  f :: [(Int, a)] -> ...
		f ((x, 1) : xs) = ...
		El tipo de f es tupla de 2 elementos. Este esta bien.
    
	g) f :: (Int -> Int) -> Int -> ...
		f a b = ...  
		El tipo de f es una funcion y un Int. Este esta bien tipado.
    
	h) f :: (Int -> Int) -> Int -> ...
		f a 3 = ...
		El tipo de f es una funcion y un Int. Este esta bien tipado.    
    
	i)  f :: (Int -> Int) -> Int -> ...
		f 0 1 2 = ...
		El tipo de f es una funcion y un Int. Este esta mal tipado ya que f usa 2 argumentos y le estoy dando 3.
--14
	a) f :: (a, b) -> b 
		f (x, y) = y
	b) f :: (a, b) -> c
		f (x,y) = z
	
	c) f :: (a -> b) -> a -> b
		f t x = y
	
	d) f :: (a -> b) -> [a] -> [b]
		f t (x:xs) = (y:ys)
	e) f :: (a -> b) -> (b -> c) -> a -> c
		f t s n = z    
--}
