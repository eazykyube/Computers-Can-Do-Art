import numpy
from PIL import Image, ImageDraw, ImageColor
import random

sizeOfSide = 512
sizeOfMatrix = 34
sizeOfRectangle = 15
sizeOfPopulation = 100
mutateRectangle = 0.00125
mutateIndividual = 1
image = Image.open('rm.png') #type:Image.Image
colors = image.getcolors(sizeOfSide*sizeOfSide)

def myRandomizer(probability):
    return random.random() <= probability

class Rectangle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = random.choice(colors)[1]

    def change(self):
        self.color = random.choice(colors)[1]

    def ideal(self):
        self.color = image.getpixel((self.y, self.x))

class Individual:
    def __init__(self):
        self.circles = self.form()
        self.points = self.getPoints()

    def form(self):
        matrix = [[0 for x in range(sizeOfMatrix)] for y in range(sizeOfMatrix)]
        for a in range(sizeOfMatrix):
            for b in range(sizeOfMatrix):
                matrix[a][b] = Rectangle(a*sizeOfRectangle+1, b*sizeOfRectangle+1)
        return matrix

    def mutate(self):
        for a in range(sizeOfMatrix):
            for b in range(sizeOfMatrix):
               if(myRandomizer(mutateRectangle)):
                   self.circles[a][b].change()
        self.points = self.getPoints()

    def createImage(self):
        newImage = Image.new("RGB", [sizeOfSide, sizeOfSide], ImageColor.getrgb("white"))
        drawing = ImageDraw.Draw(newImage)
        for idRow, row in enumerate(self.circles):
            for idCol, circle in enumerate(row):
                startX = 1 + idCol*sizeOfRectangle
                startY = 1 + idRow*sizeOfRectangle
                endX = startX + sizeOfRectangle
                endY = startY + sizeOfRectangle
                drawing.rectangle([(startX, startY), (endX, endY)], circle.color)
        return newImage

    def getPoints(self):
        myImage = self.createImage()
        arrayMyImage = numpy.array(myImage).astype(numpy.int)
        arrayImage = numpy.array(image).astype(numpy.int)
        return (numpy.abs(arrayMyImage-arrayImage).sum()/255.0*100)/arrayImage.size

    def crossover(self, indFirst, indSecond):
        for a in range(sizeOfMatrix):
            for b in range(sizeOfMatrix):
                if(myRandomizer(0.5)):
                    self.circles[a][b].color = indFirst.circles[a][b].color
                else:
                    self.circles[a][b].color = indSecond.circles[a][b].color
        self.points = self.getPoints()

    def ideal(self):
        for a in range(sizeOfMatrix):
            for b in range(sizeOfMatrix):
                self.circles[a][b].ideal()
        self.points = self.getPoints()

class Population:
    def __init__(self):
        self.individuals = self.form()

    def form(self):
        matrix = [0 for x in range(sizeOfPopulation)]
        for a in range(sizeOfPopulation):
            matrix[a] = Individual()
        return matrix

    def sort(self):
        self.individuals.sort(key=lambda x: x.points)

    def crossover(self):
        self.sort()
        for a in range(sizeOfPopulation//2-1):
            newIndividual = Individual()
            newIndividual.crossover(self.individuals[a], self.individuals[a+1])
            self.individuals[sizeOfPopulation//2+1+a] = newIndividual
        self.sort()

    def mutate(self):
        for a in range(sizeOfPopulation//2, sizeOfPopulation):
            if(myRandomizer(mutateIndividual)):
                self.individuals[a].mutate()
                self.sort()

individual = Individual()
individual.ideal()
individual.createImage().save("ideal.png")
print(individual.points)

population = Population()
for i in range(4000):
    print("Iteration no "+str(i))
    population.crossover()
    population.mutate()
    print(population.individuals[0].getPoints())
    if(i%40 == 0):
        population.individuals[0].createImage().save(str(i)+".png")










