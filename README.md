# **Bioax's Discord Bot**
This discord bot uses the [Warframe API](https://docs.warframestat.us/), [warframe.market API](https://warframe.market/api_docs), [FACEIT API](https://developers.faceit.com/docs/auth/api-keys), and the [sherlock.py library](https://github.com/sherlock-project/sherlock).
## **Commands**
### **Warframe Related**
!price \<item> **-** returns price of thing from warframe.market  
!drops \<item> **-** returns drop-tables of item  
!nightwave/nw **-** returns current nightwave challenges  
!sortie **-** returns current sortie missions  
!eidolon/cetus/earth **-** returns the state on Plains of Eidolon  
!orbvallis/fortuna/venus **-** returns the state on Orb Vallis  
!cambiondrift/cambion/deimos/necralisk **-** returns the state on Cambion Drift  

### **Faceit Related**
!stats/faceit/lifetime \<username/link> **-** returns stats of player. Takes in either a link or a case-sensitive username  
!faceitpast/statspast \<username/link> \[matches (default is 20)] **-** returns stats over past x matches, with default being 20

### **Spooky Stuff**
!pull/dox/doxx/fetch \<username> **-** Sends file of user's socials

### **Server Related**
!dm \<mention user> \<message> **-** Sends specified user a dm with given message  
!dmall \<message> **-** Sends entire server given message (must be admin)