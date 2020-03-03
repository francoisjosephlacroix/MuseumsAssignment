class WikiReferenceValidator:

    def isReferenceValid(reference):
        if (not reference.startswith("/wiki/")):
            return False
        else:
            return True
