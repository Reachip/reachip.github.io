---
layout: post
title: L'inversion de contrôle en détail avec Spring
subtitle: “Vous ne pouvez pas correctement traiter un problème tant que vous n'êtes pas correctement capables de le décrire.” - Jean-Marc Jancovici
cover-img: /assets/img/kelly-sikkema-v9FQR4tbIq8-unsplash.jpeg
thumbnail-img: /assets/img/kelly-sikkema-v9FQR4tbIq8-unsplash.jpeg
share-img: /assets/img/kelly-sikkema-v9FQR4tbIq8-unsplash.jpeg
tags: [conception, programmation, ioc, java]
---

On compare souvent la construction d'un programme écrit en programmation orientée objet comme l'immense chantier d'une maison, ou les murs de cette dernière contiennent plusieurs pièces, qui elles même contiennent plusieurs "objets" empilées et assemblées les uns aux autres et disposées à des positions bien précises.

Aujourd'hui, nous nous intéresserons à la façon dont les architectes décident de bâtir les pièces de la maison et les contenus de la pièce. En d'autres termes, dans le jargon du logiciel, comment les objets sont injectés les uns aux autres d'une manière relativement optimisée grâce à l'usage de conteneur d'inversion de contrôle (IoC).

Je tenterai d'expliquer ces concepts en codant une preuve de concept à l'aide du framework Spring. J'utiliserais le langage Kotlin afin de m'adresser au plus grand nombre d'entre vous, que vous veniez de l'écosystème Java ou autre. 

Kotlin est un langage orienté objet et fonctionnel, simple à lire et avec du sucre syntaxique. Il est aussi totalement compatible avec l'écosystème de la JVM, ce qui en fait un choix de remplacement ou de complément à Java.

# L'inversion de contrôle ?

> L'inversion de contrôle déplace les responsabilités secondaires depuis un objet vers d'autres objets qui sont dédiés à chaque responsabilité et respecte ainsi le 
> principe de responsabilité unique. - Robert C. Martin 

En d'autres termes, l'inversion de contrôle est la capacité pour un objet de contenir un autre objet en tant que propriété afin d'utiliser ces méthodes exposées. On peut arriver à une telle pratique grâce à ce qu'on appelle l'injection de dépendance.

La façon la plus commune d'injecter consiste à passer l'objet souhaité via le constructeur. Cette méthode convient dans la plupart des cas simples, mais s'avère inadapté lorsque le logiciel souhaite gagner en performance et que la complexité grandit.

Admettons que les objets *A*, *B* et *C* requièrent l'injection d'un objet *Z*. Injecter une nouvelle copie d'objet *Z* à chacun des objets demande davantage de mémoire et de ressources au niveau du système. Chaque copie doit être indépendamment gérée.

Pour combler cette problématique, on pourrait injecter des objets dont les classes possèdent des méthodes et des propretés statiques ou encore faire du passage par référence. Ces deux options sont au mieux in-maintenables sur le long terme et au pire, source de conflit pour des programmes multi-thread.

La solution la plus raisonnable est donc l'utilisation de container IOC. Ils permettent un haut niveau d'abstraction quant à l'injection optimisé de dépendance pour l'ensemble d'un programme. 

# l'IOC avec Spring

Nous expliquerons dans cet article les concepts avancés d'IOC avec le framework Spring en commençant par créer des générateurs de données aléatoires.
Pour cela, nous allons créer une interface qui représente nos fameux générateurs.

```kotlin
interface Randomizer {
    /**
     * Return random value as string
     */
    fun getAsString(): String
}
```
Nous créerons ensuite deux générateurs : Un générateur d'UUID's aléatoire, puis un générateur de nombres aléatoire.

```kotlin
class RandomNumber : Randomizer {
    override fun getAsString(): String = Random.nextInt(0, 100).toString()
}

class RandomUUID : Randomizer {
    override fun getAsString(): String = java.util.UUID.randomUUID().toString()
}
```

## Niveau 1 : Injecter une classe et utiliser ces méthodes 

Afin d'utiliser le container de Spring sur les méthodes de la classe ```RandomUUID```, nous devons tout d'abord déclarer un contexte.

```kotlin
internal class RandomUUIDScopeTest {
    @Test
    fun getAsStringSingletonScopeTest() {
        val appCtx = AnnotationConfigApplicationContext(RandomUUID::class.java)
    }
}
```

Pour utiliser ces méthodes et configurer leurs comportements, il faut annoter ces méthodes comme étant des ```@Bean``` en décrivant leur comportement via l'usage de ```@Scope```. 


Il y a deux principaux comportements pour une méthode dont la classe a été injectée : 

- Le comportement dit "singleton". Il permet de conserver le premier retour de la méthode appelante est le retour à chaque prochain appel.
- Le comportement dit "prototype". Ce dernier exécute la fonction à chaque appel sans conserver le premier retour.


Nous testerons ces deux comportements pour chacune des implémentations de l'interface ```Randomizer```. C'est pour cela que nous allons directement annoter ```@Bean``` pour une méthode qui aura le comportement "singleton" et un comportement "prototype".


```kotlin
interface Randomizer {
    /**
     * Return random value as string
     */
    fun getAsString(): String

    /**
     * Décrit un Bean ayant le comportement "singleton".
     */
    @Bean
    @Scope(value = ConfigurableBeanFactory.SCOPE_SINGLETON)
    fun getAsStringSingletonScope(): String = getAsString()

    /**
     * Décrit un Bean ayant le comportement "prototype".
     */
    @Bean
    @Scope(value = ConfigurableBeanFactory.SCOPE_PROTOTYPE)
    fun getAsStringPrototypeScope(): String = getAsString()
}
```

Testons maintenant le comportement "scope" via l'appel de la méthode ```getAsStringSingletonScope```.
On utilisera la méthode ``getBean()``` du contexte afin d'exécuter la méthode en bonne et due forme.

```kotlin
@Test
fun getAsStringSingletonScopeTest() {
    val appCtx = AnnotationConfigApplicationContext(RandomUUID::class.java)
    val uuidAsString = appCtx.getBean("getAsStringSingletonScope")

    for (loop in 0..1) {
        val nextUUIDGenerated = appCtx.getBean("getAsStringSingletonScope")
        assertTrue(uuidAsString == nextUUIDGenerated)
    }
}
```


Une fois un premier appel effectué, on appel encore deux fois de suite la méthode, puis on constate que le retour reste le même alors que la méthode doit forcément retourner un seul et unique UUID à chaque fois. Cela et dû au comportement singleton décrit dans le code source de l'interface.

Voyons mainteant le comportement dit "prototype".

```kotlin
@Test
fun getAsStringPrototypeScopeTest() {
    val appCtx = AnnotationConfigApplicationContext(RandomUUID::class.java)
    val uuidAsString = appCtx.getBean("getAsStringPrototypeScope")

    for (loop in 0..1) {
        val nextUUIDGenerated = appCtx.getBean("getAsStringPrototypeScope")
        assertFalse(uuidAsString == nextUUIDGenerated)
    }
}
```

On constate effectivement que chaque appel génère un UUID différent. Le premier appel n'est donc jamais stocké et est retourné à chaque nouveaux appels.

## Niveau 2 : Injecter une classe dans une classe et utiliser ces méthodes 

Nous allons créer une classe ```SysOutService``` qui va simplement se charger d'utiliser les ```Randomizer``` à disposition et d'afficher depuis la sortie standard. Nous devons par soucis de rigueur préciser à la JVM que cet objet implémente le comportement d'un ```Runnable```. L'objet aura la possibilité d'être exécuté via un thread. Plus d'informations ici : [https://docs.oracle.com/javase/7/docs/api/java/lang/Runnable.html](https://docs.oracle.com/javase/7/docs/api/java/lang/Runnable.html)

```kotlin
class SysOutService(val randomizer: Randomizer) : Runnable {
    override fun run() = println(randomizer.getAsString())
}
```

L'objet ```SysOutService``` n'échappe pas à la règle, nous devons faire en sorte qu'il soit retourné en tant que Bean, à la nuance que cette fois-ci, il possède une dépendance à injecter, en l'occurrence, un ```Randomizer```.

```kotlin
@Bean
fun randomUUIDBean(): Randomizer {
    return RandomUUID();
}

@Bean
fun sysOutRunnableBean(randomizer: Randomizer): Runnable {
    return SysOutService(randomizer);
}

@Test
fun runTest() {
    val appCtx = AnnotationConfigApplicationContext(SysOutServiceTest::class.java)
    val runnable: Runnable = appCtx.getBean(Runnable::class.java)

    assertDoesNotThrow("Should not throw exception") { runnable.run() }
}
```

```
output
======

ee34babd-9f37-4a67-9b80-08527faed5bc
```

Comment le container IOC a su qu'il devait injecter le bean randomUUIDBean ? En fait, Spring se base sûr ce que nous avons décrit. Ici, nous avons décrit dans notre code source un seul bean renvoyant un objet ```Randomizer``. Spring se base alors sur cette déclaration et n'en demande pas plus. 

Nous pouvons bien-sûr écrire d'autre Bean renvoyant un objet ```Randomizer```et se montrer plus précis quant à ce que doit faire le container de Spring.

```kotlin
@Bean
@Primary
fun randomUUIDBean(): Randomizer {
    return RandomUUID();
}

@Bean
fun randomNumber(): Randomizer {
    return RandomNumber();
}

@Bean
fun sysOutRunnableBean(randomizer: Randomizer): Runnable {
    return SysOutService(randomizer);
}

@Test
fun runTest() {
    val appCtx = AnnotationConfigApplicationContext(SysOutServiceTest::class.java)
    val runnable: Runnable = appCtx.getBean(Runnable::class.java);

    assertTrue((runnable as SysOutService).randomizer is RandomUUID)
    assertDoesNotThrow("Should not throw exception") { runnable.run() }
}
```

On peut par exemple utiliser l'annotation ```Primary```, qui permet de décrire l'utilisation de ce Bean en cas de choix ambigü à faire par le container.

# Avec Spring, il faut décrire afin de résoudre

Si les quelques lignes si au-dessus qui décrivent brièvement le comportement de du container sont comprises, il est dorénavant facile de comprendre que Spring s'appuie sur ce que vous décrivez dans votre code source afin d'adapter son comportement et de configurer votre application.

```java
@Configuration
public class ConfigInterceptor implements WebMvcConfigurer {
    private final HelloWorldInterceptor helloWorldInterceptor;

    public ConfigInterceptor( HelloWorldInterceptor helloWorldInterceptor) {
        this.helloWorldInterceptor = helloWorldInterceptor;
    }

    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(helloWorldInterceptor);
    }
}
```

Par exemple, la configuration d'intercepteur (synonyme de middleware) ne nécessite pas de déclarer dans un fichier de configuration l'existence de ce dernier. On le fait directement en codant.
