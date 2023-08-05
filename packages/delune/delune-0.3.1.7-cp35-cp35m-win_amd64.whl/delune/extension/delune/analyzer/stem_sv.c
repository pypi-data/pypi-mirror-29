/*  Swedish stemmer tring to remove inflectional suffixes */
#include <string.h>
#include "analyzer.h"

int stem_sv (char *word, int stem_level)
{ 
int len = strlen (word)-1;

if (len > 3) {   /*  -s  genitive form */
   if (word[len]=='s') {  
      word[len]='\0'; 
      len--;
      }
   }

if (len > 6) {   /*  -elser  -heten  */
   if ((word[len]=='r') && (word[len-1]=='e') && (word[len-2]=='s') && 
       (word[len-3]=='l') && (word[len-4]=='e')) {  
      word[len-4]='\0'; 
      return strlen (word);
      }
   if ((word[len]=='n') && (word[len-1]=='e') && (word[len-2]=='t') && 
       (word[len-3]=='e') && (word[len-4]=='h')) {  
      word[len-4]='\0'; 
      return strlen (word);
      }
   }  /* len > 6 */


if (len > 5) {   /*  -arne  -erna  -ande  -else  -aste  -orna  -aren  */
   if ((word[len]=='e') && (word[len-1]=='n') && (word[len-2]=='r') && 
       (word[len-3]=='a')) {  
      word[len-3]='\0'; 
      return strlen (word); 
      }
   if ((word[len]=='a') && (word[len-1]=='n') && (word[len-2]=='r') && 
       (word[len-3]=='e')) {  
      word[len-3]='\0'; 
      return strlen (word);
      }
   if ((word[len]=='e') && (word[len-1]=='d') && (word[len-2]=='n') && 
       (word[len-3]=='a')) {  
      word[len-3]='\0'; 
      return strlen (word);
      }
   if ((word[len]=='e') && (word[len-1]=='s') && (word[len-2]=='l') && 
       (word[len-3]=='e')) {  
      word[len-3]='\0'; 
      return strlen (word);
      }
   if ((word[len]=='e') && (word[len-1]=='t') && (word[len-2]=='s') && 
       (word[len-3]=='a')) {  
      word[len-3]='\0'; 
      return strlen (word);
      }
   if ((word[len]=='a') && (word[len-1]=='n') && (word[len-2]=='r') && 
       (word[len-3]=='o')) {  
      word[len-3]='\0'; 
      return strlen (word);
      }
   if ((word[len]=='n') && (word[len-1]=='e') && (word[len-2]=='r') && 
       (word[len-3]=='a')) {  
      word[len-3]='\0'; 
      return strlen (word);
      }
   }  /* len > 5 */


if (len > 4) {   /*  -are  comparative form */
   if ((word[len]=='e') && (word[len-1]=='r') && (word[len-2]=='a')) {  
      word[len-2]='\0'; 
      return strlen (word);
      }
      /* -ast  superlative form */
   if ((word[len]=='t') && (word[len-1]=='s') && (word[len-2]=='a')) {  
        word[len-2]='\0'; 
     return strlen (word);
      }
      /* -het  form */
   if ((word[len]=='t') && (word[len-1]=='e') && (word[len-2]=='h')) {  
        word[len-2]='\0'; 
      return strlen (word);
      }
   } /* if len > 4 */


if (len > 3) {   
              /* -{aeo}r    */
   if ((word[len]=='r') && 
      ((word[len-1]=='a') || (word[len-1]=='o') || (word[len-1]=='e'))) {  
      word[len-1]='\0'; 
      return strlen (word);
      }
    /* -en   */  
   if ((word[len-1]=='e') && (word[len]=='n')) {
      word[len-1]='\0'; 
      return strlen (word);
      }
    /* -at  */  
   if ((word[len-1]=='a') && (word[len]=='t')) {
      word[len-1]='\0'; 
      return strlen (word);
      }
    /* -te  */  
   if ((word[len-1]=='t') && (word[len]=='e')) {
      word[len-1]='\0'; 
      return strlen (word);
      }
    /* -et  */  
   if ((word[len-1]=='t') && (word[len]=='e')) {
      word[len-1]='\0'; 
      return strlen (word);
      }
   }  /* end if len > 3 */


if (len > 2) { /* -{taen}  */  
   if ((word[len]=='t') || (word[len]=='a') || 
       (word[len]=='e') || (word[len]=='n')) {
      word[len]='\0'; 
      return strlen (word);
      }
   }  /* end if len > 2 */


return strlen (word);
}


