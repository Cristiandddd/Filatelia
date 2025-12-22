export interface Lesson {
  id: string
  sectionId: string
  title: string
  description: string
  scripture?: string
  estimatedMinutes: number
  order: number
  locked: boolean
  content: LessonContent
}

export interface LessonContent {
  introduction: DialogueStep
  teaching: DialogueStep[]
  application: DialogueStep
  reflection: DialogueStep
}

export interface DialogueStep {
  id: string
  type: "narration" | "question" | "reflection" | "scripture"
  text: string
  scripture?: string
  options?: DialogueOption[]
  helpAvailable?: boolean
}

export interface DialogueOption {
  id: string
  text: string
  response: string
  followUp?: string
  isCorrect?: boolean
}

export interface LessonProgress {
  userId: string
  completedLessons: string[]
  currentLesson?: string
  lessonStates: Record<string, LessonState>
  totalTimeSpent: number
  lastUpdated: number
}

export interface LessonState {
  lessonId: string
  startedAt: number
  completedAt?: number
  currentStepId: string
  responses: Record<string, string>
  helpUsed: string[]
  timeSpent: number
}

export const LESSON_GENESIS_1: Lesson = {
  id: "genesis-1",
  sectionId: "genesis-creation",
  title: "The Creation of the World",
  description: "God brings order from chaos",
  scripture: "Genesis 1:1-2:3",
  estimatedMinutes: 16,
  order: 1,
  locked: false,
  content: {
    introduction: {
      id: "intro-1-perfected",
      type: "narration",
      text: "Have you ever stood in complete darkness? That moment before the first spark of light appears? Today we're going back to the ultimate 'before' moment - where everything began. What if I told you the first words of the Bible reveal not just how the world started, but why you matter in it?",
      options: [
        {
          id: "opt-1",
          text: "I'm ready to explore the beginning",
          response:
            "Excellent! Let's discover together how the foundation of everything shapes our understanding of God and ourselves.",
        },
        {
          id: "opt-2",
          text: "I've read Genesis before",
          response:
            "Wonderful! Even familiar ground can yield new treasures when we look closely. Let's see what fresh insights await.",
        },
        {
          id: "opt-3",
          text: "I'm curious about the creation story",
          response:
            "Perfect! You're about to encounter one of the most profound and beautiful accounts ever written.",
        },
      ],
    },
    teaching: [
      {
        id: "teach-1-perfected",
        type: "scripture",
        text: "Let's start with the most famous opening in literature:",
        scripture: '"In the beginning, God created the heavens and the earth." - Genesis 1:1',
      },
      {
        id: "teach-2-perfected",
        type: "question",
        text: "Many people wonder: Why doesn't the Bible say when God was created?",
        options: [
          {
            id: "opt-1",
            text: "God has no beginning - He's eternal",
            response:
              "CORRECT. The Bible assumes God's eternal nature rather than explaining it. He simply IS - the self-existent One who depends on nothing outside Himself. This foundational truth distinguishes the Creator from all creation, which has a beginning. God's eternity is not something to be proven but accepted as the necessary precondition for everything else that exists.",
            isCorrect: true,
          },
          {
            id: "opt-2",
            text: "Some truths are too profound for words",
            response:
              "NOT QUITE. While God's nature is indeed profound, the Bible is clear and specific about His eternal existence. The issue isn't that it's too deep for words, but that God's self-existence is presented as axiomatic - the starting point that makes everything else meaningful. Scripture repeatedly affirms 'from everlasting to everlasting, you are God' (Psalm 90:2).",
            isCorrect: false,
          },
          {
            id: "opt-3",
            text: "It distinguishes God from creation",
            response:
              "IMPORTANT but secondary. While this is true, the primary reason is more fundamental: God's eternal nature defines reality itself. Everything else is contingent and dependent; only God is necessary and self-sufficient. The distinction flows FROM His eternal nature rather than being the reason for the silence about His origin.",
            isCorrect: false,
          },
        ],
        helpAvailable: true,
      },
      {
        id: "teach-3-perfected",
        type: "narration",
        text: "Now let's look at the scene God steps into:",
      },
      {
        id: "teach-4-perfected",
        type: "scripture",
        text: "The initial condition of creation:",
        scripture:
          '"The earth was without form and void, and darkness was over the face of the deep. And the Spirit of God was hovering over the face of the waters." - Genesis 1:2',
      },
      {
        id: "teach-5-perfected",
        type: "question",
        text: "The Spirit 'hovering' - this word is used elsewhere for a bird caring for its young. What might this suggest about God's relationship to creation?",
        options: [
          {
            id: "opt-1",
            text: "God is intimately involved from the start",
            response:
              "CORRECT. The imagery of hovering conveys attentive, protective presence. Even in the chaos and formlessness, God wasn't distant but intimately engaged with His creation. Like a mother bird watching over her nest, God's Spirit was actively involved, preparing to bring forth life and order. This shows creation wasn't a mechanical act but a personal, caring work.",
            isCorrect: true,
          },
          {
            id: "opt-2",
            text: "Creation is cherished, not just made",
            response:
              "PARTIALLY CORRECT but misses the active dimension. While God does cherish creation, the hovering specifically emphasizes His active, preparatory involvement. The focus is on what God is DOING in the chaos - not just how He feels about it. The cherishing becomes evident as He speaks order and beauty into existence.",
            isCorrect: false,
          },
          {
            id: "opt-3",
            text: "There's purpose in the chaos",
            response:
              "TRUE but incomplete. The hovering does suggest purposeful engagement with the chaos, but the primary revelation is about God's personal, caring presence. The purpose emerges FROM His active involvement rather than being inherent in the chaos itself.",
            isCorrect: false,
          },
        ],
        helpAvailable: true,
      },
      {
        id: "teach-6-perfected",
        type: "narration",
        text: "Now watch how God brings order through a beautiful, repeated pattern over six days...",
      },
      {
        id: "teach-7-perfected",
        type: "scripture",
        text: "The rhythm of creation:",
        scripture:
          '"And God said, "Let there be light," and there was light. And God saw that the light was good." - Genesis 1:3-4',
      },
      {
        id: "teach-8-perfected",
        type: "question",
        text: "God speaks creation into existence. What does this tell us about His power and authority?",
        options: [
          {
            id: "opt-1",
            text: "His word has creative power",
            response:
              "CORRECT. God's speech is inherently powerful and effective. He doesn't build or craft using existing materials - His word itself brings reality into being. This demonstrates absolute sovereignty where mere declaration accomplishes His will. As Hebrews 11:3 confirms, the universe was created by God's command, showing His word is the ultimate creative force.",
            isCorrect: true,
          },
          {
            id: "opt-2",
            text: "He establishes the power of words",
            response:
              "SECONDARY application. While words do matter, this focuses on human application rather than divine revelation. The primary truth is about God's unique creative authority, not establishing a general principle about language. Human words have derivative power; God's words have inherent creative power.",
            isCorrect: false,
          },
          {
            id: "opt-3",
            text: "It connects to Jesus as the Word",
            response:
              "IMPORTANT connection but not the primary meaning here. John 1 does identify Jesus as the Word through whom all things were made, but in Genesis 1, the focus is on God's sovereign creative power through His spoken word. The Christological connection is valid but represents later revelation.",
            isCorrect: false,
          },
        ],
        helpAvailable: true,
      },
      {
        id: "teach-9-perfected",
        type: "narration",
        text: "Let's notice the pattern that develops - separation, filling, and declaration of goodness...",
      },
      {
        id: "teach-10-perfected",
        type: "scripture",
        text: "The creation of humanity:",
        scripture:
          '"Then God said, "Let us make man in our image, after our likeness." So God created man in his own image, in the image of God he created him; male and female he created them." - Genesis 1:26-27',
      },
      {
        id: "teach-11-perfected",
        type: "question",
        text: "'Let US make man in OUR image.' This plural language has fascinated readers for millennia. What might it suggest?",
        options: [
          {
            id: "opt-1",
            text: "A hint of the Trinity",
            response:
              "CORRECT. Many Christian theologians see this as an early glimpse of the triune God - Father, Son, and Spirit working together in creation. The plural language suggests divine deliberation within the Godhead, consistent with the New Testament revelation that all three persons were involved in creation (John 1:3, Colossians 1:16). This doesn't mean ancient readers understood the Trinity fully, but the language prepares for this later revelation.",
            isCorrect: true,
          },
          {
            id: "opt-2",
            text: "The majesty and complexity of God",
            response:
              "TRUE but inadequate. While God is indeed majestic and complex, the specific plural language ('us/our') suggests interpersonal relationship rather than just complexity. The biblical emphasis is on God's relational nature within Himself, not merely His incomprehensible majesty.",
            isCorrect: false,
          },
          {
            id: "opt-3",
            text: "A heavenly council",
            response:
              "LESS LIKELY interpretation. While God does consult heavenly beings elsewhere, humanity is created specifically in GOD'S image, not that of angelic beings. The consistent biblical testimony is that God alone creates humanity, making the heavenly council interpretation less compelling than the Trinitarian reading.",
            isCorrect: false,
          },
        ],
        helpAvailable: true,
      },
      {
        id: "teach-12-perfected",
        type: "narration",
        text: "Now let's consider what being 'image bearers' actually means for us...",
      },
      {
        id: "teach-13-perfected",
        type: "scripture",
        text: "Our purpose as image-bearers:",
        scripture:
          '"And God blessed them. And God said to them, "Be fruitful and multiply and fill the earth and subdue it, and have dominion over the fish of the sea and over the birds of the heavens and over every living thing that moves on the earth."" - Genesis 1:28',
      },
      {
        id: "teach-14-perfected",
        type: "question",
        text: "Based on what we've seen, what does being God's 'image' involve?",
        options: [
          {
            id: "opt-1",
            text: "Representing God's character",
            response:
              "FOUNDATIONAL but incomplete. Representing God's character is crucial, but the image involves more - it includes functional representation and relational capacity. Ancient kings placed images of themselves to represent their authority in distant territories; similarly, we represent God's rule and character in creation.",
            isCorrect: false,
          },
          {
            id: "opt-2",
            text: "Creative stewardship of creation",
            response:
              "CORRECT. This captures the functional aspect of the image. As God's image-bearers, we're called to 'subdue' and 'have dominion' - not as destructive tyrants but as wise stewards who cultivate and care for creation as God would. This reflects God's own creative, ordering work and represents His loving rule over what He made.",
            isCorrect: true,
          },
          {
            id: "opt-3",
            text: "Relational capacity like God's",
            response:
              "IMPORTANT dimension but not the primary meaning here. While we reflect God's relational nature, the creation account emphasizes our functional role as stewards. Our relational capacity flows FROM being God's image, but the initial commission focuses on our responsibility toward creation.",
            isCorrect: false,
          },
        ],
        helpAvailable: true,
      },
      {
        id: "teach-15-perfected",
        type: "narration",
        text: "Finally, God does something remarkable - He rests...",
      },
      {
        id: "teach-16-perfected",
        type: "scripture",
        text: "The seventh day:",
        scripture:
          '"And on the seventh day God finished his work that he had done, and he rested on the seventh day from all his work that he had done. So God blessed the seventh day and made it holy." - Genesis 2:2-3',
      },
      {
        id: "teach-17-perfected",
        type: "question",
        text: "Why would an all-powerful God need to 'rest'? What's really happening here?",
        options: [
          {
            id: "opt-1",
            text: "He's modeling a rhythm for us",
            response:
              "CORRECT. God establishes a pattern of work and rest that reflects His wisdom for human flourishing. The Sabbath principle isn't about God's need but about His design for creation. By resting, God sanctifies time itself and shows that productivity isn't humanity's ultimate purpose - relationship with Him is central.",
            isCorrect: true,
          },
          {
            id: "opt-2",
            text: "He's enjoying His completed work",
            response:
              "PARTIALLY TRUE but misses the purposeful aspect. While God certainly delighted in His creation, the rest primarily signifies completion and perfection rather than mere enjoyment. It's the rest of satisfaction that declares 'it is finished' - nothing needs to be added or improved.",
            isCorrect: false,
          },
          {
            id: "opt-3",
            text: "He's declaring creation 'complete'",
            response:
              "ACCURATE but secondary. The completion is indeed signaled by the rest, but the greater significance is the establishment of a pattern for human life. The Sabbath becomes a creation ordinance, built into the very fabric of reality for humanity's benefit and God's glory.",
            isCorrect: false,
          },
        ],
        helpAvailable: true,
      },
      {
        id: "teach-preview-1-perfected",
        type: "narration",
        text: "FASCINATING PREVIEW: John's Gospel begins with the exact same words - 'In the beginning' - but reveals something astonishing about who was there with God from the start. We'll explore this profound connection when we reach the New Testament!",
      },
    ],
    application: {
      id: "app-1-perfected",
      type: "reflection",
      text: "If God created everything 'very good,' why is there so much suffering and evil in the world? Does this mean creation is flawed or something went wrong?",
    },
    reflection: {
      id: "refl-1-perfected",
      type: "reflection",
      text: "You are made in God's image with inherent dignity and purpose. How does this truth change how you view yourself and treat others this week?",
    },
  },
}