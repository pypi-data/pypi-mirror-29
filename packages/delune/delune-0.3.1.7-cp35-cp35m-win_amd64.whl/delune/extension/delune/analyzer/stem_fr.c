/*  French stemmer tring to remove inflectional and derivational suffixes */
#include <string.h>
#include "analyzer.h"

static int normfrenchword(char *word);
static char * removeDoublet(char *word);

int stem_fr (char *word, int stem_level)
{ 
int len = strlen (word)-1;

if (len > 4) {
   if (word[len]=='x') {
      if (word[len-1]=='u' && word[len-2]=='a' && word[len-3]!='e') {
         word[len-1]='l';  /*  chevaux -> cheval  */
         }                 /*  error :  travaux -> traval but not travail  */
      word[len]='\0';      /*  anneaux -> anneau,  neveux -> neveu  */
      len--;               /*  error :  aulx -> aul but not ail (rare)  */
      }
   }                       /*  error :  yeux -> yeu but not oeil (rare)  */
if (len > 2) {
   if (word[len]=='x') {
      word[len]='\0';      /*  peaux -> peau,  poux -> pou  */
      len--;               /*  error :  affreux -> affreu */
      }                    
   }

if (len > 2 && word[len]=='s') {  /*  remove final --s --> -- */
   word[len]='\0';
   len--;
   }

if (len > 8) {  /* --issement  -->   --ir */
      if (word[len]=='t'   && word[len-1]=='n' && word[len-2]=='e' && 
          word[len-3]=='m' && word[len-4]=='e' && word[len-5]=='s' && 
          word[len-6]=='s' && word[len-7]=='i') {
         word[len-6]='r';       /* investissement --> investir */
         word[len-5]='\0';
      return(normfrenchword(word));
      }
   }

if (len > 7) {  /* ---issant  -->   ---ir */
      if (word[len]=='t'   && word[len-1]=='n' && word[len-2]=='a' && 
          word[len-3]=='s' && word[len-4]=='s' && word[len-5]=='i') {
         word[len-4]='r';     /* assourdissant --> assourdir */
         word[len-3]='\0';
      return(normfrenchword(word));
      }
   }

if (len > 5) {    /* --ement  -->   --e */
      if (word[len]=='t'   && word[len-1]=='n' && word[len-2]=='e' && 
          word[len-3]=='m' && word[len-4]=='e') {
         word[len-3]='\0';       /* pratiquement --> pratique */
         if (word[len-5]=='v' && word[len-6]=='i') {
            word[len-5]='f';     /* administrativement --> administratif */
            word[len-4]='\0';
            }
      return(normfrenchword(word));
      }
   }

if (len > 10) {    /* ---ficatrice  -->   --fier */
      if (word[len]=='e'   && word[len-1]=='c' && word[len-2]=='i' && 
          word[len-3]=='r' && word[len-4]=='t' && word[len-5]=='a' &&
          word[len-6]=='c' && word[len-7]=='i' && word[len-8]=='f') {
         word[len-6]='e';
         word[len-5]='r';
         word[len-4]='\0';   /* justificatrice --> justifier */
      return(normfrenchword(word));
      }
   }

if (len > 9) {    /* ---ficateur -->   --fier */
      if (word[len]=='r'   && word[len-1]=='u' && word[len-2]=='e' && 
          word[len-3]=='t' && word[len-4]=='a' && word[len-5]=='c' &&
          word[len-6]=='i' && word[len-7]=='f') {
         word[len-5]='e';
         word[len-4]='r';
         word[len-3]='\0';   /* justificateur --> justifier */
      return(normfrenchword(word));
      }
   }

if (len > 8) {    /* ---catrice  -->   --quer */
      if (word[len]=='e'   && word[len-1]=='c' && word[len-2]=='i' && 
          word[len-3]=='r' && word[len-4]=='t' && word[len-5]=='a' &&
          word[len-6]=='c') {
         word[len-6]='q';
         word[len-5]='u';
         word[len-4]='e';
         word[len-3]='r';
         word[len-2]='\0';   /* educatrice--> eduquer */
      return(normfrenchword(word));
      }
   }

if (len > 7) {    /* ---cateur -->   --quer */
      if (word[len]=='r'   && word[len-1]=='u' && word[len-2]=='e' && 
          word[len-3]=='t' && word[len-4]=='a' && word[len-5]=='c') {
         word[len-5]='q';
         word[len-4]='u';
         word[len-3]='e';
         word[len-2]='r';
         word[len-1]='\0';   /* communicateur--> communiquer */
      return(normfrenchword(word));
      }
   }

if (len > 7) {    /* ---atrice  -->   --er */
      if (word[len]=='e'   && word[len-1]=='c' && word[len-2]=='i' && 
          word[len-3]=='r' && word[len-4]=='t' && word[len-5]=='a') {
         word[len-5]='e';
         word[len-4]='r';
         word[len-3]='\0';   /* accompagnatrice--> accompagner */
      return(normfrenchword(word));
      }
   }

if (len > 6) {    /* ---ateur  -->   --er */
      if (word[len]=='r'   && word[len-1]=='u' && word[len-2]=='e' && 
          word[len-3]=='t' && word[len-4]=='a') {
         word[len-4]='e';
         word[len-3]='r';
         word[len-2]='\0';   /* administrateur--> administrer */
      return(normfrenchword(word));
      }
   }

if (len > 5) {    /* --trice  -->   --teur */
      if (word[len]=='e'   && word[len-1]=='c' && word[len-2]=='i' && 
          word[len-3]=='r' && word[len-4]=='t') {
         word[len-3]='e';
         word[len-2]='u';
         word[len-1]='r';  /* productrice --> producteur */
         word[len]='\0';   /* matrice --> mateur ? */
         len--;
      }
   }

if (len > 4) {    /* --i?me  -->   -- */
      if (word[len]=='e' && word[len-1]=='m' && word[len-2]=='?' && 
          word[len-3]=='i') {
         word[len-3]='\0';     
      return(normfrenchword(word));
      }
   }

if (len > 6) {    /* ---teuse  -->   ---ter */
      if (word[len]=='e'   && word[len-1]=='s' && word[len-2]=='u' && 
          word[len-3]=='e' && word[len-4]=='t') {
         word[len-2]='r';      
         word[len-1]='\0';       /* acheteuse --> acheter */
      return(normfrenchword(word));
      }
   }

if (len > 5) {    /* ---teur  -->   ---ter */
      if (word[len]=='r'   && word[len-1]=='u' && word[len-2]=='e' && 
          word[len-3]=='t') {
         word[len-1]='r';      
         word[len]='\0';       /* planteur --> planter */
      return(normfrenchword(word));
      }
   }

if (len > 4) {    /* --euse  -->   --eu- */
      if (word[len]=='e' && word[len-1]=='s' && word[len-2]=='u' && 
          word[len-3]=='e') {
         word[len-1]='\0';       /* poreuse --> poreu-,  plieuse --> plieu- */
      return(normfrenchword(word));
      }
   }

if (len > 7) {    /* ------?re  -->   ------er */
      if (word[len]=='e' && word[len-1]=='r' && word[len-2]=='?') {
         word[len-2]='e';
         word[len-1]='r';
         word[len]='\0';  /* bijouti?re --> bijoutier,  caissi?re -> caissier */
      return(normfrenchword(word));
      }
   }

if (len > 6) {    /* -----ive  -->   -----if */
      if (word[len]=='e' && word[len-1]=='v' && word[len-2]=='i') {
         word[len-1]='f';   /* but not convive */
         word[len]='\0';   /* abrasive --> abrasif */
      return(normfrenchword(word));
      }
   }

if (len > 3) {    /* folle or molle  -->   fou or mou */
      if (word[len]=='e' && word[len-1]=='l' && word[len-2]=='l' && 
          word[len-3]=='o' && (word[len-4]=='f' || word[len-4]=='m')) {
         word[len-2]='u';
         word[len-1]='\0';  /* folle --> fou */
      return(normfrenchword(word));
      }
   }

if (len > 8) {    /* ----nnelle  -->   ----n */
      if (word[len]=='e'   && word[len-1]=='l' && word[len-2]=='l' && 
          word[len-3]=='e' && word[len-4]=='n' && word[len-5]=='n') {
         word[len-4]='\0';  /* personnelle --> person */
      return(normfrenchword(word));
      }
   }

if (len > 8) {    /* ----nnel  -->   ----n */
      if (word[len]=='l'   && word[len-1]=='e' && word[len-2]=='n' && 
          word[len-3]=='n') {
         word[len-2]='\0';  /* personnel --> person */
      return(normfrenchword(word));
      }
   }

if (len > 3) {    /* --?te  -->  et */
      if (word[len]=='e' && word[len-1]=='t' && word[len-2]=='?') {
         word[len-2]='e';  
         word[len]='\0';  /* compl?te --> complet */
         len--;
      }
   }

if (len > 7) {    /* -----ique  -->   */
      if (word[len]=='e' && word[len-1]=='u' && word[len-2]=='q' && 
          word[len-3]=='i') {
         word[len-3]='\0';  /* aromatique --> aromat */
         len = len-4;
      }
   }

if (len > 7) {    /* -----esse -->    */
      if (word[len]=='e' && word[len-1]=='s' && word[len-2]=='s' && 
          word[len-3]=='e') {
         word[len-2]='\0';    /* faiblesse --> faible */
      return(normfrenchword(word));
      }
   }

if (len > 6) {    /* ---inage -->    */
      if (word[len]=='e' && word[len-1]=='g' && word[len-2]=='a' && 
          word[len-3]=='n' && word[len-4]=='i') {
         word[len-2]='\0';  /* patinage --> patin */
      return(normfrenchword(word));
      }
   }

if (len > 8) {    /* ---isation -->   - */
      if (word[len]=='n'   && word[len-1]=='o' && word[len-2]=='i' && 
          word[len-3]=='t' && word[len-4]=='a' && word[len-5]=='s' && 
          word[len-6]=='i') {
         word[len-6]='\0';     /* sonorisation --> sonor */
         if (len > 11 && word[len-7]=='l' && word[len-8]=='a' && word[len-9]=='u') 
            word[len-8]='e';  /* ritualisation --> rituel */
      return(normfrenchword(word));
      }
   }

if (len > 8) {    /* ---isateur -->   - */
      if (word[len]=='r'   && word[len-1]=='u' && word[len-2]=='e' && word[len-3]=='t' &&
          word[len-4]=='a' && word[len-5]=='s' && word[len-6]=='i') {
         word[len-6]='\0';  /* colonisateur --> colon */
      return(normfrenchword(word));
      }
   }

if (len > 7) {    /* ----ation -->   - */
      if (word[len]=='n'   && word[len-1]=='o' && word[len-2]=='i' && 
          word[len-3]=='t' && word[len-4]=='a') {
         word[len-4]='\0';  /* nomination --> nomin */
      return(normfrenchword(word));
      }
   }

if (len > 7) {    /* ----ition -->   - */
      if (word[len]=='n'   && word[len-1]=='o' && word[len-2]=='i' && 
          word[len-3]=='t' && word[len-4]=='i') {
         word[len-4]='\0';  /* disposition --> dispos */
      return(normfrenchword(word));
      }
   }

/* various other suffix */
   return(normfrenchword(word));
}

static char * removeDoublet(char *word)
{ 
int len = strlen (word)-1;
int i, position;
char currentChar;

if (len > 3) {
   currentChar = word[0];
   position = 1;
   while (word[position]) {
      if (currentChar == word[position]) {
         i = position-1;
         while (word[i] != '\0') {
            word[i] = word[i+1];
            i++;
            }
         }  /* end if */
         else {
            currentChar = word[position];
            position++;
              }
      }  /* end while */
   } /* end if len */
return(word);
}


static int
normfrenchword(char *word)
{ 
int len = strlen (word)-1;

   if (len > 3) {
      //removeAllFEAccent(word); 
      if (!removeLatinAccents (word)) return 0;
      removeDoublet(word);   
      len = strlen (word)-1;  
   }

   if (len > 3) {
      if (word[len]=='e' && word[len-1]=='i')
        {word[len-1]='\0';len = len -2;}
   }
   if (len > 3) {
      if (word[len]=='r')
        {word[len]='\0';len--;}
      if (word[len]=='e')
        {word[len]='\0';len--;}
/*    if (word[len]=='?')  */
      if (word[len]=='e')
        {word[len]='\0';len--;}
      if (word[len] == word[len-1])
         word[len]='\0';
   }
//return(word);         
return strlen (word);
}


