removal_list = ( ',', "'", '"', '.', '!', '?', ':' )

def rule1( text ):
    for remov in removal_list:
        text = text.replace(remov, "")
    return text

def noyo( text ):
    newtext = text.replace('ё', 'е')
    return newtext
