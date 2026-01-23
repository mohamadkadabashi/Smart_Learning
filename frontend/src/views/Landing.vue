<template>
  <div class="landing-page">

    <header class="container pt-5 mt-4 pb-0">
      <div class="row align-items-center">
        <div class="col-lg-6 mb-5 mb-lg-0" style="z-index: 10; position: relative;">
          <h1 class="display-5 fw-bold mb-3 text-dark">
            Wandle deine Skripte <br />
            in interaktive Tests um.
          </h1>
          <p class="lead text-secondary mb-4">
            <b>SmartLearning</b> generiert aufbauend auf deinen Dokumenten und Vorlesungsunterlagen sofort
            passende Fragen. <br />
            Lerne effizienter, verfolge deinen Fortschritt und sei besser vorbereitet auf Prüfungen.
          </p>
        </div>
        <div class="col-lg-6 d-flex justify-content-center position-relative">
          <div class="image-wrapper-hero">
            <img src="/assets/images/dashboard-mockup.png" alt="App Dashboard Vorschau" class="hero-img">
          </div>
        </div>
      </div>
    </header>

    <section class="bg-light py-5 mt-0 position-relative" style="z-index: 1;">
      <div class="container pt-4">
        <div class="text-center mb-5">
          <h2 class="fw-bold">Dein Weg zur perfekten Prüfungsvorbereitung</h2>
        </div>

        <div class="row g-4">
          <div class="col-md-4" v-for="(step, index) in steps" :key="index">
            <div class="card h-100 border-0 shadow-sm p-4 text-center step-card">
              <div class="icon-circle mb-3 mx-auto">
                <img :src="step.icon" :alt="step.title" class="step-icon">
              </div>
              <h4 class="fw-bold mb-3">{{ step.title }}</h4>
              <p class="text-secondary">{{ step.description }}</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="py-5">
      <div class="container text-center">
        <div class="mb-4">
          <h2 class="fw-bold m-0">Bereit zum Starten?</h2>
        </div>
        <button class="primary cta-btn" @click="$router.push('/login-or-register')">
          Jetzt Account erstellen
        </button>
      </div>
    </section>

    <section class="bg-light py-5">
      <div class="container">
        <div class="text-center mb-5">
          <h2 class="fw-bold" id="help">Hilfe</h2>
        </div>
        <div class="row g-4 justify-content-center">
          <div class="col-12" v-for="(faq, f) in faqs" :key="'faq-' + f">
            <div class="card h-100 border-0 p-4 shadow-sm faq-card">
              <h5 class="fw-bold text-primary-orange mb-2">
                <img src="/assets/images/faq.svg" width="20" class="faq-icon" />
                {{ faq.question }}
              </h5>
              <p class="text-secondary mb-0" style="padding-left: 37px;" v-html="faq.answer"></p>
            </div>
          </div>
        </div>
      </div>
    </section>

  </div>
</template>

<script>
export default {
  name: "Landing",
  data() {
    return {
      steps: [
        {
          title: "Material wählen",
          description: "SmartLearning benutzt deine lokalen Daten als Wissensbasis",
          icon: "/assets/images/document-text-sharp.svg"
        },
        {
          title: "Test konfigurieren",
          description: "Wähle zwischen Fragentypen und lege die Fragenanzahl fest.",
          icon: "/assets/images/switches.svg"
        },
        {
          title: "Smarter lernen",
          description: "Starte mit deinen Tests. Halte deine Streak am Leben und verbessere deine Erfolgsquote.",
          icon: "/assets/images/rocket.svg"
        }
      ],
      faqs: [
        {
          question: "Tests",
          answer: "Ein Test wird auf Basis deiner eigenen Dokumente generiert. Du kannst ihn individuell an deine Bedürfnisse anpassen. <br><br><b>1. Starten:</b> Klicke “Neuen Test erstellen” während du der Dashboard-Seite bist.<br><b>2. Dokumente hochladen:</b> Wähle deine lokalen Dokumente, die als Wissensbasis dienen.<br><b>3. Modul zuweisen:</b> Wähle das dazu passende Modul für den Test aus.<br><b>4. Konfiguration:</b> Vergib einen einzigartigen Namen, um den Test später wiederzufinden.<br><b>5. Typen:</b> Bestimme die Aufgabentypen (z.B. Single Choice).<br><b>6. Umfang:</b> Lege die gewünschte Anzahl der Fragen fest.<br><b>7. Generieren:</b> Klicke auf “Test erstellen” und es werden automatisch die passenden Übungsfragen in einem Test erstellt."
        },
        {
          question: "Module",
          answer: "Module dienen als übergeordnete Ordner für deine verschiedenen Fachbereiche (z.B. Mathe, Physik). Sie helfen dir, deine Tests sauber nach Themen zu sortieren. <br><br><b>1.</b> Klicke auf das Plus-Icon (+) im Dashboard neben “Deine Module”. <br><b>2.</b> Gib dem Modul einen einzigartigen Namen. <br><b>3.</b> Nach dem Speichern erscheint das Modul in deiner Übersicht “Deine Module”.<br><b>4.</b> Wenn du neue Tests erstellst, kannst du sie in deinem Modul speichern."
        },
        {
          question: "Dashboard",
          answer: "Dein Dashboard zeigt dir auf einen Blick, wie effektiv du lernst: <br><br><b>- Lernzeit:</b> Die investierte Zeit in der aktuellen Woche im Vergleich zur Vorwoche. <br><b>- Erfolgsquote:</b> Dein prozentualer Anteil an richtig beantworteten Fragen. <br><b>- Streak:</b> Die 🔥 zeigt dir, wie viele Tage in Folge du bereits aktiv gelernt hast. <br><b>- Tests bestanden:</b> Die Anzahl der Tests, die du mit mindestens 60% bestanden hast. <br><b>- Tagesziel:</b> Der Fortschrittsbalken visualisiert, wie nah du an deinem selbst festgelegten Tagesziel bist."
        },
        {
          question: "Einstellungen & Profil",
          answer: "In den Einstellungen kannst du dein Lernerlebnis personalisieren: <br><br><b>- Passwort & Persönliche Daten:</b> Hier kannst du deine Anmeldedaten und persönliche Informationen aktualisieren.<br><b>- Tagesziel anpassen:</b> Passe die Anzahl der täglichen Tests an, die du erreichen möchtest. <br><b>- Streak:</b> Aktiviere oder deaktiviere deine Streak-Anzeige im Dashboard."
        }
      ]
    };
  }
};
</script>

<style scoped>
.text-primary-orange {
  color: #E88D46;
}

.primary {
  background-color: #E88D46;
  color: white;
  border: none;
  padding: 10px 24px;
  border-radius: 8px;
  font-weight: 600;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.cta-btn {
  border-radius: 50px;
  padding: 14px 40px;
  font-size: 1.2rem;
}

.image-wrapper-hero {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: flex-end;
}

.hero-img {
  width: 90%;
  margin-bottom: -50px;
  position: relative;
}

.step-card {
  border-radius: 16px;
  transition: transform 0.3s ease;
}

.step-card:hover {
  transform: translateY(-5px);
}

.faq-card {
  border-radius: 16px;
}

.icon-circle {
  width: 70px;
  height: 70px;
  background-color: #E88D46;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.step-icon {
  width: 32px;
  height: 32px;
  filter: brightness(0) invert(1);
}

.faq-icon {
  width: 32px;
  height: 32px;
}

@media (max-width: 991px) {
  .hero-img {
    width: 100%;
    margin-bottom: 0;
  }
}
</style>