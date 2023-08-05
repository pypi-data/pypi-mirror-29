/*  Finnish stemmer tring to remove inflectional suffixes */
#include <string.h>
#include "analyzer.h"

static char *removeDoubleKPT(char *word);
static char *finnishStep1(char *word);
static char *finnishStep2(char *word);
static char *finnishStep3(char *word);
static char *norm_finnish(char *word);
static char *norm2_finnish(char *word);


#define IsVowel(c) ('a'==(c)||'e'==(c)||'i'==(c)||'o'==(c)||'u'==(c)||\
                    'y'==(c))


int stem_fi (char *word, int stem_level)
{ 
int len = strlen (word)-1;

if (len > 2) {
   //removeFinnishAccent(word);
  if (!removeLatinAccents (word)) return 0;
   finnishStep1(word);
   finnishStep2(word);
   finnishStep3(word);
   norm_finnish(word);
   norm2_finnish(word);
   }
return strlen (word);
}


static char * norm_finnish (char *word)
{ 
int len = strlen (word)-1;

if (len > 4) {   /* -hde  -> -ksi  */
   if ((word[len]=='e') && (word[len-1]=='d') && (word[len-2]=='h')) {  
      word[len-2]='k';  
      word[len-1]='s';  
      word[len]='i';  
      }
   }  /* end if len > 4 */
if (len > 3) {   /* -ei  -> -  */
   if ((word[len]=='i') && (word[len-1]=='e')) {  
      word[len-1]='\0';
      return(word);  
      }
   if ((word[len]=='t') && (word[len-1]=='a')) {  
      word[len-1]='\0';
      return(word);  
      }
   }  /* end if len > 3 */
if (len > 2) {   /* plural    -t  or -(aeiouy)i */
   if ((word[len]=='t') || (word[len]=='s') || (word[len]=='j') 
      || (word[len]=='e') || (word[len]=='a')) {  
      word[len]='\0';  
      }
   else {
/*      if ((word[len]=='i') && (IsVowel(word[len-1]))) { */
      if ((word[len]=='i')) {   
         word[len]='\0';
         }
      }
   } /* end if (len > 2) */ 
return(word);
}


static char * norm2_finnish (char *word)
{ 
int len = strlen (word)-1;

if (len > 7) {   /* -e, -o,  -u */
   if ((word[len]=='e') || (word[len]=='o') || (word[len]=='u')) { 
      word[len]='\0';  
      len--;
      }
   }
if (len > 3) {   /* plural    -i  */
   if (word[len]=='i') {  
      word[len]='\0';  
      }
   removeDoubleKPT(word);
   } /* end if (len > 3) */ 
return(word);
}


static char * removeDoubleKPT(char *word)
{ 
int len = strlen (word)-1;
int i, position;
char currentChar;

if (len > 3) {
   currentChar = word[0];
   position = 1;
   while (word[position]) {  /*  remove double kk pp tt  */
      if ((currentChar==word[position]) && ((currentChar=='k') ||
              (currentChar=='p') || (currentChar=='t'))) {
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


static char * finnishStep1 (char *word)
{ 
int len = strlen (word)-1;

if (len > 7) {
 /*    -kin  */
   if ((word[len]=='n') && (word[len-1]=='i') && (word[len-2]=='k')) {
         word[len-2]='\0';
      return(finnishStep1(word));
      }
 /*    -ko  */
   if ((word[len]=='o') && (word[len-1]=='k')) {
         word[len-1]='\0';
      return(finnishStep1(word));
      }
   } /* end if (len > 7) */ 
if (len > 10) {
 /*    -dellinen  for adjective  */
   if ((word[len]=='n') && (word[len-1]=='e') && (word[len-2]=='n')
      && (word[len-3]=='i') && (word[len-4]=='l') && (word[len-5]=='l')
      && (word[len-6]=='e') && (word[len-7]=='d')) {
         word[len-7]='\0';
      return(word);
      }
 /*    -dellisuus  for adverb  */
   if ((word[len]=='s') && (word[len-1]=='u') && (word[len-2]=='u')
      && (word[len-3]=='s') && (word[len-4]=='i') && (word[len-5]=='l')
      && (word[len-6]=='l') && (word[len-7]=='e') && (word[len-8]=='d')) {
         word[len-8]='\0';
      return(word);
      }
   } /* end if (len > 10) */ 
return(word);         
}


static char *finnishStep2 (char *word)
{ 
int len = strlen (word)-1;

if (len > 4) {
 /*    -lla  */
   if ((word[len]=='a') && (word[len-1]=='l') && (word[len-2]=='l')) {
         word[len-2]='\0';
      return(word);
      }
 /*    -tse  */
   if ((word[len]=='e') && (word[len-1]=='s') && (word[len-2]=='t')) {
         word[len-2]='\0';
      return(word);
      }
 /*    -sti  */
   if ((word[len]=='i') && (word[len-1]=='t') && (word[len-2]=='s')) {
         word[len-2]='\0';
      return(word);
      }
 /*    -ni  */
   if ((word[len]=='i') && (word[len-1]=='n')) {
         word[len-1]='\0';
      return(word);
      }
 /*    -a  if -aa  */
   if ((word[len]=='a') && (word[len-1]=='a')) {
         word[len]='\0';
      return(word);
      }
   } /* end if (len > 4) */ 
return(word);         
}


static char * finnishStep3 (char *word)
{ 
int len = strlen (word)-1;

if (len > 7) {
 /* genetive -nnen  -s  */
   if ((word[len]=='n') && (word[len-1]=='e') && 
            (word[len-2]=='n') && (word[len-3]=='n')) {
         word[len-3]='s';
         word[len-2]='\0';
      return(word);
      }
 /* essive -ntena  -s  */
   if ((word[len]=='a') && (word[len-1]=='n') && (word[len-2]=='e') && 
            (word[len-3]=='t') && (word[len-4]=='n')) {
         word[len-4]='s';
         word[len-3]='\0';
      return(word);
      }
 /*  -tten  -s  */
   if ((word[len]=='n') && (word[len-1]=='e') && (word[len-2]=='t') && 
            (word[len-3]=='t')) {
         word[len-3]='\0';
      return(word);
      }
 /* genitive plural   -eiden  -s  */
   if ((word[len]=='n') && (word[len-1]=='e') && 
       (word[len-2]=='d') && (word[len-3]=='i') && (word[len-4]=='e')) {
         word[len-4]='\0';
      return(word);
      }
   }
if (len > 5) {
 /* komitatiivi plural   -neen  */
   if ((word[len]=='n') && (word[len-1]=='e') && 
            (word[len-2]=='e') && (word[len-3]=='n')) {
         word[len-3]='\0';
      return(word);
      }
/* illatiivi   -siin,  etc.  */
   if ((word[len]=='n') && (word[len-1]=='i') && 
            (word[len-2]=='i') && (word[len-3]=='n')) {
         word[len-3]='\0';
      return(word);
      }
/* illatiivi   -seen,  etc.  */
   if ((word[len]=='n') && (word[len-1]=='e') && 
            (word[len-2]=='e') && (word[len-3]=='s')) {
         word[len-3]='\0';
      return(word);
      }
/* illatiivi   -h?n,  etc.  */
   if ((word[len]=='n') && (IsVowel(word[len-1])) && 
            (word[len-2]=='h')) {
         word[len-2]='\0';
      return(word);
      }
/* genitive plural   -teen,  etc.  */
   if ((word[len]=='n') && (word[len-1]=='e') && 
            (word[len-2]=='e') && (word[len-3]=='t')) {
         word[len-3]='\0';
      return(word);
      }
 /* genitive plural   -den  -s  */
   if ((word[len]=='n') && (word[len-1]=='e') && 
            (word[len-2]=='d')) {
         word[len-2]='s';
         word[len-1]='\0';
      return(word);
      }
 /* genitive plural   -ksen  -s  */
   if ((word[len]=='n') && (word[len-1]=='e') && 
            (word[len-2]=='s') && (word[len-3]=='k')) {
         word[len-3]='s';
         word[len-2]='\0';
      return(word);
      }
 /* komitatiivi plural   -neni  */
   if ((word[len]=='n') && (word[len-1]=='e') && 
            (word[len-2]=='n') && (word[len-3]=='i')) {
         word[len-3]='\0';
      return(word);
      }
 /* inessiivi   -ssa  */
   if ((word[len]=='a') && (word[len-1]=='s') && (word[len-2]=='s')) {
         word[len-2]='\0';
      return(word);
      }
 /* elatiivi   -sta  */
   if ((word[len]=='a') && (word[len-1]=='t') && (word[len-2]=='s')) {
         word[len-2]='\0';
      return(word);
      }
 /* adessiivi   -lla  */
   if ((word[len]=='a') && (word[len-1]=='l') && (word[len-2]=='l')) {
         word[len-2]='\0';
      return(word);
      }
 /* ablatiivi   -lta  */
   if ((word[len]=='a') && (word[len-1]=='t') && (word[len-2]=='l')) {
         word[len-2]='\0';
      return(word);
      }
 /* abessiivi   -tta  */
   if ((word[len]=='a') && (word[len-1]=='t') && (word[len-2]=='t')) {
         word[len-2]='\0';
      return(word);
      }
 /* translatiivi   -ksi  */
   if ((word[len]=='i') && (word[len-1]=='s') && (word[len-2]=='k')) {
         word[len-2]='\0';
      return(word);
      }
 /* allatiivi   -lle  */
   if ((word[len]=='e') && (word[len-1]=='l') && (word[len-2]=='l')) {
         word[len-2]='\0';
      return(word);
      }
   } /* end if (len > 5) */ 
if (len > 4) {
/* essiivi   -na  */
   if ((word[len]=='a') && (word[len-1]=='n')) {    
      word[len-1]='\0';
      return(word);
      }
/* komitatiivi   -ne-  */
   if ((word[len]=='e') && (word[len-1]=='n')) {    
      word[len-1]='\0';
      return(word);
      }
   if ((word[len]=='i') && (word[len-1]=='e') && (word[len-2]=='n')) {
      word[len-2]='\0';
      return(word);
      }
   } /* end if (len > 4) */ 
if (len > 3) {
/* partitiivi   -(t,j)a  */
   if ((word[len]=='a') && ((word[len-1]=='t') || (word[len-1]=='j'))) {    
      word[len-1]='\0';
      return(word);
      }
   if (word[len]=='a') {   
      word[len]='\0';
      return(word);
      }
/* illatiivi   -an, -en, -on, -in, -un, -yn, etc.  */
   if ((word[len]=='n') && ((word[len-1]=='a') || (word[len-1]=='e')
              || (word[len-1]=='o') || (word[len-1]=='i')
              || (word[len-1]=='u') || (word[len-1]=='y'))) {    
      word[len-1]='\0';
      return(word);
      }
/* genetiivi or instruktiivi   -n  */
   if (word[len]=='n') {   
      word[len]='\0';
      return(word);
      }
   } /* end if (len > 3) */ 
return(word);         
}


