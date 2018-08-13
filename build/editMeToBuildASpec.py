import sys
sys.path.append('..') #this allows us to import from ../resources
from resources.testspecification import TestSpecification

spec = TestSpecification()

spec.Name = "AFunTest"

spec.setNumberOfTests(10)

spec.setNumberOfPages(12)
spec.setNumberOfVersions(4)

spec.setIDPages([1,2])
## Always do ID Pages first.
spec.addToSpec('f',[3,4],9)
spec.addToSpec('f',[5,6],12)
spec.addToSpec('f',[7,8],12)
spec.addToSpec('f',[9,10],6)
spec.addToSpec('f',[11,12],6)

spec.writeSpec()
spec.printSpec()