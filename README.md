# EMMET 2.0 – Projektbeskrivning

Vi utvecklar EMMET 2.0, en autonom räddningsrobot för tävlingen RoboCupJunior Rescue Line. Målet är att vår robot ska följa en svart linje genom en utmanande bana,
identifiera och samla upp offer samt transportera dem till rätt plats i en evakueringszon – snabbt och helt på egen hand.

## Bakgrund

RoboCupJunior Rescue Line är en tävling där autonoma robotar genomför ett simulerat
räddningsuppdrag. Banan är uppbyggd av moduler och innehåller bland annat korsningar,
luckor, farthinder, ojämn terräng och hinder som roboten måste ta sig förbi. I banans
slutskede finns en evakueringszon, där offer i form av kulor ska samlas upp och sorteras. Hela uppdraget ska genomföras utan mänsklig inblandning.

## Mål

- Följa linjen stabilt och mjukt genom hela banan.
- Ta oss förbi banans hinder och svåra avsnitt utan att fastna.
- Identifiera och samla upp offren.
- Leverera offren till rätt plats i evakueringszonen.
- Genomföra uppdraget helt autonomt och på kortast möjliga tid.

## Hårdvara

- Raspberry Pi 5
- Kameramodul för Raspberry Pi
- Pololu QTR-8A reflexiv sensorarray (8 sensorer)
- Raspberry Pi Build HAT
- LEGO SPIKE-motorer

## Teknisk lösning

Vår styrning bygger på två samverkande delar:

- **Sensorlagret** läser av linjens position under roboten. Med hjälp av en
  PID-regulator hålls roboten centrerad på linjen och kan följa den exakt.
- **Kameran** blickar framåt längs linjen för att förutse dess form och gör att
  roboten kan köra mjukare och effektivare. Vi använder också kameran för att känna
  igen banans gröna inslag vid bestämda svängar.

Hur vi ska kombinera sensor- och kamerainformationen är ännu under utveckling. Även
mekanismen för att samla upp kulorna återstår att färdigställa.

## Projektstatus

Vi är under aktiv utveckling. Vår kamerabaserade linjedetektion och igenkänning av
banans gröna element fungerar och testas. Kvar att utveckla är sensorinläsning,
PID-reglering, motorstyrning och uppsamlingsmekanism, samt att samordna delarna till
en komplett autonom robot.

## Om oss

Vi är ett studentlag som tillsammans utvecklar EMMET 2.0 inför tävlingen.