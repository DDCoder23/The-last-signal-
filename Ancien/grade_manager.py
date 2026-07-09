def gestionnaire_de_grade(joueur,n=None):
    def decorateur(func):
        def fonction_interne(*args, **kwargs):
            if n is None:
                pass
            return func(*args, **kwargs)
        return fonction_interne
    return decorateur

def gestionnaire_de_vehicule(joueur,n=None):
  @gestionnaire_de_grade(joueur,n)
  def decorateur(func):
      def fonction_interne(*args, **kwargs):
          if n is None:
             pass
          return func(*args, **kwargs)
      return fonction_interne
  return decorateur

def gestionnaire_de_batiments(joueur,n=None):
  @gestionnaire_de_grade(joueur,n)
  def decorateur(func):
      def fonction_interne(*args, **kwargs):
          if n is None:
             pass
          return func(*args, **kwargs)
      return fonction_interne
  return decorateur
def manage(joueur_getter):
    def decorateur(func):
        def fonction_interne(self, *args, **kwargs):
            joueur = joueur_getter(self)

            wrapped_func = gestionnaire_de_vehicule(joueur, joueur.grade)(
                gestionnaire_de_batiments(joueur, joueur.grade)(func)
            )

            # Appelle la fonction décorée
            return wrapped_func(self, *args, **kwargs)
        return fonction_interne
    return decorateur


