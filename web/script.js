const chatWindow = document.querySelector('#chatWindow');
const chatForm = document.querySelector('#chatForm');
const userInput = document.querySelector('#userInput');
const quickActions = document.querySelector('#quickActions');
const restartButton = document.querySelector('#restartChat');
const template = document.querySelector('#messageTemplate');

const clone = (value) =>
  typeof structuredClone === 'function' ? structuredClone(value) : JSON.parse(JSON.stringify(value));

const fallbackKnowledge = {
  brand: 'Felo',
  support_contact: {
    email: 'support@felo.example',
    phone: '+7 (495) 000-00-00',
    telegram: '@felo_support'
  },
  products: [
    {
      id: 'focus-spray',
      name: 'Felo Focus Спрей',
      summary:
        'Компактный спрей для мгновенной концентрации и повышения работоспособности.',
      price_rub: 1290,
      flavors: ['мята и лайм'],
      availability: 'В наличии',
      key_ingredients: ['Ноотропный комплекс', 'Гуарана', 'L-теанин'],
      recommended_for: ['концентрация', 'работа за компьютером', 'студенты'],
      benefits: [
        'Улучшает концентрацию внимания в течение 5-10 минут после применения',
        'Помогает бороться с усталостью в конце рабочего дня',
        'Удобный формат спрея, который всегда можно взять с собой'
      ],
      how_to_use: '1-2 распыления под язык до 3 раз в день.',
      faq: [
        {
          question: 'Можно ли использовать вместе с кофе?',
          answer:
            'Да, но рекомендуем уменьшить порцию кофеина, чтобы избежать перевозбуждения.'
        },
        {
          question: 'Сколько длится эффект?',
          answer: 'В среднем 2-3 часа в зависимости от индивидуальной чувствительности.'
        }
      ]
    },
    {
      id: 'energy-gummies',
      name: 'Felo Energy Жевательные пастилки',
      summary: 'Витаминные пастилки для поддержания тонуса в течение дня.',
      price_rub: 990,
      flavors: ['манго', 'клюква'],
      availability: 'Ограниченное количество',
      key_ingredients: ['Экстракт женьшеня', 'Кофеин', 'Витамины группы B'],
      recommended_for: ['энергия', 'спорт', 'утренний подъем'],
      benefits: [
        'Постепенное высвобождение энергии без резкого падения',
        'Без сахара и искусственных красителей',
        'Каждая пастилка содержит дневную норму витаминов B6 и B12'
      ],
      how_to_use: '1-2 пастилки утром или перед тренировкой.',
      faq: [
        {
          question: 'Можно ли принимать вечером?',
          answer: 'Не рекомендуем употреблять за 6 часов до сна, чтобы не нарушить режим.'
        },
        {
          question: 'Сколько пастилок в упаковке?',
          answer: '40 пастилок, рассчитанных на 3-4 недели употребления.'
        }
      ]
    },
    {
      id: 'calm-tea',
      name: 'Felo Calm Травяной чай',
      summary: 'Успокаивающий травяной сбор для снижения стресса и улучшения сна.',
      price_rub: 850,
      flavors: ['ромашка и мелисса'],
      availability: 'В наличии',
      key_ingredients: ['Мелисса', 'Ромашка', 'Лаванда', 'Магний'],
      recommended_for: ['сон', 'стресс', 'вечерний отдых'],
      benefits: [
        'Помогает расслабиться после насыщенного дня',
        'Поддерживает естественный цикл сна',
        'Не вызывает сонливость утром'
      ],
      how_to_use: 'Заваривать 1 пакетик в горячей воде (90°C) и настаивать 5 минут.',
      faq: [
        {
          question: 'Можно ли пить ежедневно?',
          answer: 'Да, чай подходит для ежедневного употребления курсами по 3-4 недели.'
        },
        {
          question: 'Есть ли ограничения по возрасту?',
          answer: 'Рекомендуется взрослым и подросткам старше 14 лет.'
        }
      ]
    },
    {
      id: 'immunity-shot',
      name: 'Felo Immunity Shot',
      summary: 'Концентрированный напиток для поддержки иммунитета в сезон простуд.',
      price_rub: 1390,
      flavors: ['облепиха с имбирем'],
      availability: 'Предзаказ',
      key_ingredients: ['Витамин C', 'Цинк', 'Экстракт эхинацеи', 'Бета-глюканы'],
      recommended_for: ['иммунитет', 'межсезонье', 'восстановление'],
      benefits: [
        'Укрепляет защитные функции организма',
        'Удобная порционная упаковка',
        'Без добавленного сахара'
      ],
      how_to_use: 'Взболтать, пить по одному шоту утром 5 дней подряд.',
      faq: [
        {
          question: 'Можно ли давать детям?',
          answer:
            'Подходит с 12 лет, перед применением детям рекомендуется консультация врача.'
        },
        {
          question: 'Когда появится в наличии?',
          answer: 'Поставки ожидаются на следующей неделе, можно оформить предзаказ.'
        }
      ]
    }
  ],
  shipping: {
    moscow: 'Доставка по Москве и МО курьером в течение 1-2 дней.',
    regions: 'Отправляем СДЕК и Почтой России, сроки 3-7 дней.',
    pickup: 'Самовывоз из шоурума у м. Курская по предварительному бронированию.'
  },
  payment: [
    'Онлайн-оплата картой на сайте',
    'Система быстрых платежей',
    'Наличными курьеру'
  ],
  return_policy:
    'Вы можете вернуть или обменять товар в течение 14 дней при сохранении упаковки.',
  delivery_cost: {
    moscow: 'Бесплатно от 2000 ₽, иначе 250 ₽.',
    regions: 'От 300 ₽ в зависимости от выбранной службы.',
    pickup: 'Всегда бесплатно.'
  }
};

let knowledge = clone(fallbackKnowledge);

async function init() {
  await loadKnowledge();
  greet();
}

async function loadKnowledge() {
  try {
    const response = await fetch('../data/products.json', { cache: 'no-store' });
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    const data = await response.json();
    if (data?.products?.length) {
      knowledge = clone(data);
    }
  } catch (error) {
    console.warn('Не удалось загрузить products.json, используется встроенный набор данных.', error);
    knowledge = clone(fallbackKnowledge);
  }
}

function greet() {
  addBotMessage(
    'Здравствуйте! Я помогу подобрать продукты Felo под вашу задачу. Расскажите, что хотите улучшить: энергию, концентрацию, сон или иммунитет?'
  );
  addBotMessage(
    'Вы также можете спросить про конкретный продукт, условия доставки, оплату или как сделать предзаказ.'
  );
}

function addMessage(role, content, { html = false } = {}) {
  const fragment = template.content.cloneNode(true);
  const article = fragment.querySelector('.message');
  const bubble = fragment.querySelector('.bubble');
  const paragraph = fragment.querySelector('p');

  article.classList.add(role === 'user' ? 'user' : 'bot');

  if (html) {
    paragraph.innerHTML = content;
  } else {
    paragraph.textContent = content;
  }

  chatWindow.appendChild(fragment);
  chatWindow.scrollTo({ top: chatWindow.scrollHeight, behavior: 'smooth' });
}

function addBotMessage(text, options) {
  addMessage('bot', text, options);
}

function addUserMessage(text) {
  addMessage('user', text);
}

function formatPrice(price) {
  return new Intl.NumberFormat('ru-RU').format(price);
}

function findProductByName(query) {
  if (!query) return null;
  const normalized = query.toLowerCase();

  const synonymMap = {
    spray: 'focus-spray',
    спрей: 'focus-spray',
    focus: 'focus-spray',
    фокус: 'focus-spray',
    пастилки: 'energy-gummies',
    gummies: 'energy-gummies',
    энергия: 'energy-gummies',
    energy: 'energy-gummies',
    чай: 'calm-tea',
    calm: 'calm-tea',
    сон: 'calm-tea',
    immunity: 'immunity-shot',
    иммунитет: 'immunity-shot',
    shot: 'immunity-shot'
  };

  const productBySynonym = synonymMap[normalized];
  if (productBySynonym) {
    return knowledge.products.find((product) => product.id === productBySynonym) ?? null;
  }

  return (
    knowledge.products.find((product) => {
      const nameMatch = product.name.toLowerCase().includes(normalized);
      const recommendedMatch = product.recommended_for.some((tag) => tag.toLowerCase().includes(normalized));
      return nameMatch || recommendedMatch;
    }) ?? null
  );
}

function detectNeed(text) {
  const normalized = text.toLowerCase();
  const needs = [
    {
      key: 'energy',
      patterns: ['энерг', 'бодр', 'заряд', 'утро', 'спорт', 'трениров']
    },
    {
      key: 'focus',
      patterns: ['концент', 'фокус', 'работ', 'учеб', 'экзам', 'память']
    },
    {
      key: 'sleep',
      patterns: ['сон', 'расслаб', 'вечер', 'уснуть', 'стресс']
    },
    {
      key: 'immunity',
      patterns: ['иммун', 'простуд', 'болеть', 'витамин', 'защит']
    }
  ];

  for (const need of needs) {
    if (need.patterns.some((pattern) => normalized.includes(pattern))) {
      return need.key;
    }
  }

  return null;
}

function renderProductCard(product) {
  const listItems = [
    `<dt>Формат и вкус</dt><dd>${product.flavors.join(', ')}</dd>`,
    `<dt>Главное</dt><dd>${product.summary}</dd>`,
    `<dt>Преимущества</dt><dd>${product.benefits.join('; ')}</dd>`,
    `<dt>Как принимать</dt><dd>${product.how_to_use}</dd>`,
    `<dt>Статус</dt><dd>${product.availability}</dd>`
  ].join('');

  return `
    <div class="product-card">
      <h3>${product.name}</h3>
      <p><strong>${formatPrice(product.price_rub)} ₽</strong></p>
      <dl>${listItems}</dl>
    </div>
  `;
}

function listProducts() {
  const listHtml = knowledge.products
    .map((product) => `• <strong>${product.name}</strong> — ${product.summary}`)
    .join('<br/>');

  addBotMessage('Наш ассортимент сейчас выглядит так:\n' + knowledge.products.map((product) => `${product.name} — ${formatPrice(product.price_rub)} ₽`).join('\n'));
  addBotMessage(`Подробно:<br/>${listHtml}`, { html: true });
}

function getRecommendation(needKey) {
  const recommendations = {
    energy: {
      prompt: 'Для поддержки энергии обратите внимание на эти продукты:',
      filter: (product) => product.recommended_for.some((tag) => tag.includes('энерг') || tag.includes('спорт'))
    },
    focus: {
      prompt: 'Для концентрации и продуктивности подойдут:',
      filter: (product) => product.recommended_for.some((tag) => tag.includes('концент') || tag.includes('работ'))
    },
    sleep: {
      prompt: 'Чтобы расслабиться и наладить сон, у нас есть:',
      filter: (product) => product.recommended_for.some((tag) => tag.includes('сон') || tag.includes('стресс'))
    },
    immunity: {
      prompt: 'Для поддержки иммунитета рекомендуем:',
      filter: (product) => product.recommended_for.some((tag) => tag.includes('иммун') || tag.includes('восстанов'))
    }
  };

  const config = recommendations[needKey];
  if (!config) return false;

  const products = knowledge.products.filter(config.filter);
  if (!products.length) return false;

  addBotMessage(config.prompt);
  products.forEach((product) => addBotMessage(renderProductCard(product), { html: true }));
  addBotMessage('Если нужен другой формат, скажите что именно вам важнее — вкус, скорость действия или условия приема.');
  return true;
}

function handleGeneralQuestions(text) {
  const normalized = text.toLowerCase();

  if (/(доставк|курьер|самовывоз)/.test(normalized)) {
    addBotMessage(
      `Доставка: ${knowledge.shipping.moscow}\nРегионально: ${knowledge.shipping.regions}\nСамовывоз: ${knowledge.shipping.pickup}`
    );
    addBotMessage(
      `Стоимость доставки: Москва — ${knowledge.delivery_cost.moscow}, регионы — ${knowledge.delivery_cost.regions}, самовывоз — ${knowledge.delivery_cost.pickup}.`
    );
    return true;
  }

  if (/(оплат|платеж|карто|сбп)/.test(normalized)) {
    addBotMessage('Мы принимаем:');
    knowledge.payment.forEach((method) => addBotMessage(`• ${method}`));
    return true;
  }

  if (/(возврат|обмен|гарант)/.test(normalized)) {
    addBotMessage(knowledge.return_policy);
    return true;
  }

  if (/(консульт|связ|контакт|телефон)/.test(normalized)) {
    const contact = knowledge.support_contact;
    addBotMessage(
      `Можете написать нам на ${contact.email}, позвонить ${contact.phone} или написать в телеграм ${contact.telegram}.`
    );
    return true;
  }

  if (/(предзаказ|когда|налич)/.test(normalized) && normalized.includes('иммун')) {
    const immunity = knowledge.products.find((product) => product.id === 'immunity-shot');
    if (immunity) {
      addBotMessage(
        `Сейчас ${immunity.name.toLowerCase()} доступен по предзаказу. ${immunity.availability}. Можем закрепить за вами упаковку.`
      );
    }
    return true;
  }

  if (/(спасибо|благодар)/.test(normalized)) {
    addBotMessage('Спасибо, что обратились! Если появятся вопросы, я всегда рядом.');
    return true;
  }

  if (/(как заказать|заказ|оформить|купить)/.test(normalized)) {
    addBotMessage(
      'Чтобы оформить заказ, напишите ваш номер телефона и удобный способ связи. Мы подтвердим наличие и отправим ссылку на оплату.'
    );
    return true;
  }

  return false;
}

function handleProductRequest(text) {
  const product = findProductByName(text);
  if (!product) return false;

  addBotMessage(renderProductCard(product), { html: true });

  const faqText = product.faq
    .map((item) => `<strong>${item.question}</strong><br/>${item.answer}`)
    .join('<br/><br/>');
  addBotMessage(faqText, { html: true });
  addBotMessage('Хотите узнать про сочетание с другими продуктами или оформить заказ?');

  return true;
}

function handleFallback(text) {
  addBotMessage(
    'Я могу рассказать про ассортимент Felo, цены, условия доставки и помочь с подбором по вашей цели. Попробуйте уточнить, например: «Нужен продукт для энергии утром» или «Расскажи про Felo Calm». '
  );
  if (!chatWindow.querySelector('.product-card')) {
    addBotMessage('Для начала вот короткий список наших бестселлеров:');
    knowledge.products.slice(0, 2).forEach((product) => addBotMessage(renderProductCard(product), { html: true }));
  }
}

function processInput(text) {
  const trimmed = text.trim();
  if (!trimmed) return;

  addUserMessage(trimmed);

  if (/(привет|здравств|добрый)/i.test(trimmed)) {
    addBotMessage('Здравствуйте! Чем могу быть полезен сегодня?');
  }

  if (handleProductRequest(trimmed)) return;

  const need = detectNeed(trimmed);
  if (need && getRecommendation(need)) return;

  if (handleGeneralQuestions(trimmed)) return;

  if (trimmed.toLowerCase().includes('ассортимент') || trimmed.toLowerCase().includes('список')) {
    listProducts();
    return;
  }

  handleFallback(trimmed);
}

chatForm.addEventListener('submit', (event) => {
  event.preventDefault();
  const text = userInput.value;
  userInput.value = '';
  processInput(text);
});

quickActions.addEventListener('click', (event) => {
  const target = event.target;
  if (!(target instanceof HTMLButtonElement)) return;
  const intent = target.dataset.intent;
  if (!intent) return;

  const intentMap = {
    list: 'Покажи все продукты',
    need_energy: 'Мне нужен продукт для энергии',
    need_focus: 'Хочу прокачать концентрацию',
    need_sleep: 'Хочу лучше засыпать',
    need_immunity: 'Нужно поддержать иммунитет'
  };

  const phrase = intentMap[intent];
  if (phrase) {
    processInput(phrase);
  }
});

restartButton.addEventListener('click', () => {
  chatWindow.innerHTML = '';
  greet();
});

init();
