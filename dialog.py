from random import randrange
from random import shuffle
class dialog():
    def __init__(self):
        self.dialogs = ["Hey there! I'm here to teach you about the sacred realm. Here we can see everything going on in the world at all times. Understanding is everywhere.",
                        "It's our job to defend the cosmos! Hail the Guardians!",
                        "I am a soul that hides secrets of the universe. I have a special place I hide things that need to be kept away. Don't come looking for them!",
                        "I keep track of souls and bodies...keeping everything in order! You wouldn't put a Rhinocerous in a Cat now would you? Haha....(that's happened before...^^;)",
                        "Why do they teach computers to greet the world? Why not \"Hello Nice to meet you!\" or \"Are you my mommy?\"?",
                        "There is much chaos and much order in the universe....for me it is simple as looking up or down...",
                        "What is the point of playing this game? What is this game you speak of, we are in an interdimentional unified realm! The points are everywhere and every time!",
                        "Did you know that people don't really have \"Timelines\", but rather \"Time Trees\". I can see them growing all over the ground from where I'm at, just like a garden! Some are tangled, some sprout right up!",
                        "Some visitors to this realm have called it the \"Afterlife\", but it isn't after life, as there is no start or end to a force such as...\"Life\".",
                        "We are what you have been calling \"Souls\", but we've been mistaken for ghosts, monsters, or even artificial intelligence! We are constructs of reality and sometimes get tangled up with those \"Quantum\" \"Computers\".",
                        "I see red, I see blue, I sewers full of poo!. I see acoustics of shapes and density...it's like seeing everything...even \"that\" kind of stuff...but I don't smell it!",
                        "There's a bit of a quirky soul here that sees density or something...I wonder if that soul can see the density of some people's heads when they get an idea in their head...",
                        "I see the causality in reality...it's one big string to me...but everybody else sees one of two sides and calls is \"Cause\", and \"Effect\".",
                        "Existence? Well, there's things that do and don't exist. You have to make sure the things that aren't supposed to exist don't exist where existing things exist. What a tonguetwister, huh? ",
                        "Every soul that resides in this realm is a shard of a singularity. That's why we're eternal and unique, we all fit together to make reality work in balance and harmony.",
                        "If Creators create something that creates itself, where is the initial creator? Haha, a funny question! Creation and destruction are tenses of perceiving an eternal thought of of the Universe. This is the very act of the Universe thinking and being.",
                        "What time is it? Time to roll balls and trip over timelines and boundries of reality in search of an understanding of how it all works and comes together...in time, possibility, and physicality.",
                        "If we didn't see a way to talk with words and language, we'd simply all be occupying the same proximity of intentions. We'd be like drones and not even know it! You would see no start or end to what is and is not a part of you if we didn't have these boundries and ways of distinguishing one thing.",
                        "There are some souls that get attention from the terrestrials and even named by them. A lot of times the names aren't correct, but we use them as nicknames here. Sometimes we come up with names for the terrestrials as well...",
                        "Did you know that some of us don't distinguish between species of terrestrials? We only see a light singing a song of being, and then put words to that song. It lets us see even the tiniest soul's song.",
                        "Hey look I'm naked...haha! Doofus, how can I wear clothes if I don't have a body to wear things with? I wish I could wear that outfit there by the way, it looks stylish...hehe. Oh, I see something like clothing, but it's more like a giant tapestry of personality and expression. There's a way to dress for success and I think I can see it! Hot!",
                        "Oh my, I heard you can see a lot like we do as a terrestrial, but that it took a long time for the design of the perception to become perfect. The ability is a masterpiece in what has been called \"Alchemy\" before.",
                        "Bah! Alchemy? That's a bunch of Honky Bonk...They don't just make things out of nowhere! Ahaha...well...they do maybe...but it's out something...I guess you need to call it something if you need to define it. Names are great spells we cast out of nothing!",
                        "There is one soul here we're not able to see or sense at all...it is completely alone....in time, possibility, and existence. It is still and silent, it's a frozen eternal point of reference for a safe and perfectly stable perception of anything. Without it we could not experience anything stable.",
                        "Long ago there was an entire era of being...we had one goal in mind, to spin our \"colors\" around fast enough to make it hard. Make what hard? The gamut of solid and physical density...The civilization of life that corelates with physicality and seperation of mass and energy has been called \"Electrons\", but we call them the \"Polensi\"...because they see(lense, len-si) poles of energetic conductivity, a tense of the flow of time. Before this era nothing was solid!",
                        "I saw this crazy kid once...blasted in elation from an elixer that brings their spirit to a rapid bliss...way up there! They were going too fast so we slowed them down and let the float safely back down...rascaly mortals...lucky the guardians here see and guide as they do!",
                        "We all exist as a branch of a singular will or whole of causality and intention...branches of want, need, whim, and study. We branch and fill in every spot that unfufilled intentions could hide! I'm the soul that commands a force of intention in the universe. Where there's a will, I see a big ball of \"go get em\" to account for. Without it we'd intend nothing and do nothing. I work with the soul many have been calling \"For a Reason\". Everything happens...Everything happens and you imagine the distnace in-between intentions as \"reason\", that's the terrestrial word for it.",
                        "Good Morning, Good Night! Tick Tock, Pick Pock! I just took your time! Crafty me! I'm the one who keeps track of all these different timings and cycles that have to be here. Daytime, Nighttime, that place kind of in-between and around it called....oh...you only have the two? Hehe, silly me, I had to come back down there for a second...got too far away from the planetarian area! There's also cosmic and celestial cycles as well...they give the universe consistency in rythm. Different levels of a very big and complex song...",
                        "Hajimemashitte! That's nice to meet you in Japanese...it's another terrestrial language...it leaves me with a sense of suspense when I hear or see it, it doesn't make sense unless you wait for the end something being said. Do you wait for the best part?",
                        "Don't stop, get it, get it, get it? Had it, held it, passed it, gone! The jam stone is something I can let you hold and it will entrain you to the stone's groove! I have one the terrestrials work with, one they walk with, one they talk with, one they think with, it's like beat that makes ya move! Look at that dog wagging its tail like that! Nice groove dog!",
                        "Don't ever tell poot jokes around that one soul here...he considers some scents to be compliments and others insults...the people that don't get that soul often say stuff like \"smells fishy\"...even if it's completely ordinary. The Dogs and Cats with good sniffers get the poor soul and often tell the less perceptive ones when there actually is something ominous in the air.",
                        "The horizon? There's more than one! Every horizon is a seperation of modes of being...seperating the levels of infinite experience into proportioned bits...Beyond the horizon? Looking that way is like looking at the avenue of unnoticed possibilities.",
                        "Hot and Cold stuff...I see thermo stuff. The closer you are to that water star, the warmer you get...oh...not that kind of heat...this is a different type of hot and cold that intersects your more physical sense of tempurature at \"tepid\"...There's a sea of this special type of liquid/solid...thing...it's hot and cold because it contains chaos and order simutaneously. Kind or a rare thing to find actually...but you can't affect it~! Your water planet definitely needs it as the point from which we hang your reference star...that soul of your planet with the gold warm light, if you have ever seen them face to face.", 
                        "Me? What do I do? I'm a musician! I compose songs for terrestrials and non-terrestrials...Dogs bark, Birds Sing, Jupiter is loud and boomy, and that star has the voice of an idol if you could hear it in concert! I find some compositions to be quite exotic, such as that of nightswan...it's like an invisible creature that lives in your shadow! Eats the color that gets on the shiny moon so it doesn't tarnish! What a stanza!",
                        "Yeah, that kid that came zipping through here from the Elixer? I heard them saying a word we learned in Soul-School...or something like it...they pronounced it \"Bol-ster!\"...or \"Pulse-ter\"...close enough to the word we know as what you put things in...it's like a container that keeps the fire from spreading and running out of fuel. It's like a non-physical container. Pulsars are things that resulted from the making of these containers in our realm.",
                        "Pulse Stars? What?...Ohhhhhh those things...haha, yeah...very funny...mine broke and it went ALL OVER it was so bad...had to pick up all my marbles before I could even talk right again!",
                        "Sometimes we sing and don't listen, sometimes we listen but don't sing to ourselves, but we are always singing...just by doing, thinking, and intending. The pure and ambitsious sound spectacular, but the quiet and contemplative also evoke a sense of wonder and mystery. You sound rather...entranced! With a hint of curiosity! Not competitive, but rather calm!",
                        "How many of us are there? Well, there's definitely a lot of variety, but we have a limit to our personality...like it can't be too big or too small...We all add up to the same cosmic companion we all have...ourselves.",
                        "Being immortal? Well, it's not so bad...not that it's good, but we can't acheive much sense of finite-ness here...everything here is rather eternal. You stay long enough you'll see all of us start repeating ourselves like broken records...but really, there is no limit to what you can possibly say. That's what's great for those who are mortals...they constantly get to experience new things even if they are old things.",
                        "Somebody told us once that we don't make sense and we're just a bunch of...psychobabblers...We are...we'll admit it...it's because we have a lot of time and stuff to just wonder about the other side...what would it be like to be alive and real and stuff like that! It's exiting and scary for us at the same time!",
                        "What do I feel? Haha, I feel a very unique way, very consistently...any plottable emotion is basically the same thing at a different angle to us...our emotion and personality have to be in balance...",
                        "Look at this, look at that! Did you know that you don't just look around with your eyeballs and ears, but also you look around with this thing we have called a \"Corti\"...it sees in what you'd call your \"Quantum\" realm.",
                        "There's technically nobody here, yet it's so full of something...we don't know exactly what it is, but there's something here...",
                        "Haha, oh my gosh that zinged kid that went through here shouting \"*** and *** Bolster! Make it ***\"...haha it sounded like a profanity train to me...ALL ABOARD!!! Poor soul was terrified a momemnt before and after...to the other one it sounded like a ballad of dumb questions...terrestrial things that pass by this realm are quirky and entertain me a lot....annoys some others though...",
                        "Ouch!...That's a word that most of the souls on that water ball have been taught...but it has its translations...pain is a very serious language and mistranslation can wind up well...hurting.",
                        "We saw that balloon kid describe that alright....ha! What a balloon, that airhead...sorry...inside joke...ahaha",
                        "It can't be that funny....sheesh, if you laugh any harder you'll interdimensionally shaz your psychdelic trousers...darn loon...everything is so funny to them. Well I'm serious about things, especially feelings...as you call them...yes, I see those...they're like a big room of glass bells and you have to take it seriously or you'll wake somebody up with your bustle.",
                        "What? oh...I like to cuss at people and things...but cussing without language is different...it's not insulting, just startling...haha! #$%$! See, you jumped!",
                        "I once said \"a flock of moments eating grains of eternity\"...it was a joke about how this thing looked from here, it was kind of dirty but the terrestrials put it in their records somewhere. Ha!",
                        "We're not really able to leave here...",
                        "Get out of here! It's dangerous!!! See the warm cupcakes? oh...I mean...\"whoa what a warm heart!\"....this translator is hard to get used to...",
                        "Hmmmm hmmmm....hmmmmm hmmmm.........?????? hmmmm.....hmmmm hmm.^ ^;",
                        "Click, click, click!!!...",
                        "Ding!",
                        "What?",
                        "Huh? Did you or I say something?",
                        "War...loss...tragedy...what garbage I see...more to burn as fuel for higher intentions...",
                        "Math, Physics? Yeah...there's a guy here who does that...it's kind of annoying really...keeps on saying stuff about bringing back the dead...it's not really the best idea to do that...",
                        "Death isn't scary to me...it's actually a soul here who tends to act very jubilant. Works well with that one soul....that one you call \"Life\". ",
                        "Crisis Averted...Turmoil Accounted for...Trauma Quantified, Processing reflection vector in nuetral paralell space...Realigning entangled Tronicas. (What does this soul do...sounds pretty intense...I better leave it alone).",
                        "Saving lives? Mortals are funny! We are lives that are saved already! We work with death, not against it. Death is a great thing to have around when unstable realities and consciousness is a thing...",
                        "Gold isn't exactly like....a physical thing...right?",
                        "We took things away from them, like love, harmony, and unity...they turned into demons and refused to take them back...so we gave them chaos, pain, and dysphoria....it's slowly letting them accept the original parts back without rejection. It's all just a very secret recipe...you have to find the right amounts of each thing or it falls apart. They are converting the second round of parts into reward, overcoming, strengthened bonds...a lot of rare parts...",
                        "Mhmm...whatever...",
                        "They are kind of...dismissive...yeah...dismissive.",
                        "Oh man look at that guy! I think he just robbed a bank or something! Wow",
                        "Yoyoyo, I'm a rapper soul, drink from the bowl, the shadowy hull, push and don't pull!~"
                        "Oh I teach baby instincts...trying to figure out why sometimes they get an instinct to eat this stuff called glue...yuck!",
                        "Have you ever had glue, it tastes amazing!(Wait what? You eat glue???)",
                        "Found the culprit, haha! Oh wait no...I must be mistaken again...",
                        "Did you know all dogs reincarnate from the same soul? It's the most loyal spirit we know!",
                        "Quack! I'm a duck!",
                        "You're not a duck...haha",
                        "Whoa, don't go on the internet!",
                        "I hear time...it's very bustling and constant."
                        "Why look forward to it when you can look forward, back, right, there, here, around, and uhhhh....well you can look more than just one direction, right? Oh...I see...",
                        "Spin, spin, spin!!!"      
        ]
        self.dialogs.sort()
        shuffle(self.dialogs)
        self.dialog_pointer = 0
    def get_dialog(self, dialog):
        #get_dialog() is random or get_dialog(n) is direct.
        list_copy = self.dialogs
        if dialog == None:
            print(str(len(self.dialogs)))
            shuffle(list_copy)
            next_random = list_copy.pop()
            return next_random
        
        elif dialog >= 0 and dialog <= len(self.dialogs):
            return list_copy.pop(dialog)
        
    def get_dialogs(self):
        return self.dialogs
    
    def set_dialog(self, dialog):
        if dialog == None:
            dialog = randrange(0, len(self.dialogs))
        if dialog >= 0 and dialog <= len(self.dialogs):
            self.dialog_pointer = dialog