# 🔐 GUIA: CONFIGURAR SECRETS NO GITHUB E STREAMLIT CLOUD

## 🎯 O QUE VOCÊ PRECISA

Este guia mostra como configurar sua chave API do DeepSeek em diferentes plataformas, **SEM** expor a chave no código.

---

## 📋 ÍNDICE

1. [Streamlit Cloud (Recomendado para Deploy)](#streamlit-cloud)
2. [GitHub Codespaces (Para Desenvolvimento)](#github-codespaces)
3. [GitHub Actions (Para CI/CD)](#github-actions)
4. [Local (.env - Para Desenvolvimento Local)](#local-env)

---

## 🚀 1. STREAMLIT CLOUD

### Para fazer deploy do dashboard no Streamlit Cloud:

### Passo 1: Preparar o Código

✅ Código já está preparado! O arquivo `ai_chatbot.py` lê automaticamente de `st.secrets`.

### Passo 2: Deploy no Streamlit Cloud

1. **Acesse:** https://share.streamlit.io/
2. **Faça login** com sua conta GitHub
3. **Clique em** "New app"
4. **Configure:**
   - Repository: `honacleon/dashboard-BUSINESS`
   - Branch: `master`
   - Main file path: `Products/Business/main.py`

### Passo 3: Configurar Secrets

1. **Após deploy, clique no app**
2. **Clique no menu (⋮) → Settings**
3. **Vá em "Secrets"**
4. **Cole este conteúdo:**

```toml
[deepseek]
api_key = "sk-715eb85d01dc41ff96963231e69dc82d"
api_url = "https://api.deepseek.com/v1"
model = "deepseek-chat"
max_tokens = 2050
temperature = 0.7
```

5. **Clique em "Save"**
6. **App reinicia automaticamente** ✅

### Verificar se Funcionou:

- Acesse o chatbot no app
- Vá em "⚙️ Configurações Avançadas"
- Deve mostrar: "✅ IA Real Ativa - DeepSeek"

---

## 💻 2. GITHUB CODESPACES

### Para desenvolvimento direto no navegador:

### Passo 1: Abrir Codespace

1. **Vá no repositório:** https://github.com/honacleon/dashboard-BUSINESS
2. **Clique em** "Code" → "Codespaces" → "Create codespace on master"

### Passo 2: Configurar Secrets

**OPÇÃO A: Secret do Repositório (Recomendado)**

1. **No GitHub, vá em:** Settings → Secrets and variables → Codespaces
2. **Clique em** "New repository secret"
3. **Configure:**
   - Name: `DEEPSEEK_API_KEY`
   - Value: `sk-715eb85d01dc41ff96963231e69dc82d`
4. **Clique em** "Add secret"

**OPÇÃO B: Arquivo .env no Codespace**

```bash
# No terminal do Codespace:
cd Products/Business
cp .env.example .env
nano .env
# Cole sua chave e salve (Ctrl+O, Enter, Ctrl+X)
```

### Passo 3: Rodar o Dashboard

```bash
cd Products/Business
python -m streamlit run main.py
```

---

## 🔧 3. GITHUB ACTIONS

### Para CI/CD (testes automatizados, builds, etc.):

### Passo 1: Configurar Secret

1. **Vá no repositório:** https://github.com/honacleon/dashboard-BUSINESS
2. **Settings → Secrets and variables → Actions**
3. **Clique em** "New repository secret"
4. **Configure:**
   - Name: `DEEPSEEK_API_KEY`
   - Value: `sk-715eb85d01dc41ff96963231e69dc82d`
5. **Clique em** "Add secret"

### Passo 2: Usar no Workflow

Crie `.github/workflows/test.yml`:

```yaml
name: Test Dashboard

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          cd Products/Business
          pip install -r requirements.txt

      - name: Run tests
        env:
          DEEPSEEK_API_KEY: ${{ secrets.DEEPSEEK_API_KEY }}
        run: |
          cd Products/Business
          pytest tests/
```

---

## 🏠 4. LOCAL (.env)

### Para desenvolvimento na sua máquina:

### Já Está Configurado! ✅

Você já tem o arquivo `.env` com sua chave.

### Para outros desenvolvedores:

```bash
# 1. Clonar repositório
git clone https://github.com/honacleon/dashboard-BUSINESS.git
cd dashboard-BUSINESS/Products/Business

# 2. Copiar .env.example
copy .env.example .env

# 3. Editar .env (cole sua chave)
notepad .env

# 4. Rodar dashboard
python -m streamlit run main.py
```

---

## 🔄 ORDEM DE PRIORIDADE

O código busca a chave nesta ordem:

```
1️⃣ Streamlit Secrets (st.secrets)
   ↓ (se não encontrar)
2️⃣ Variáveis de Ambiente (os.environ)
   ↓ (se não encontrar)
3️⃣ Arquivo .env (dotenv)
   ↓ (se não encontrar)
4️⃣ Modo Simulado
```

Isso significa que o **mesmo código funciona em todos os ambientes!** 🎉

---

## 📝 TEMPLATE PARA COLAR

### Para Streamlit Cloud / GitHub Codespaces:

```toml
[deepseek]
api_key = "sk-715eb85d01dc41ff96963231e69dc82d"
api_url = "https://api.deepseek.com/v1"
model = "deepseek-chat"
max_tokens = 2050
temperature = 0.7
```

### Para GitHub Actions (como variável):

```
DEEPSEEK_API_KEY=sk-715eb85d01dc41ff96963231e69dc82d
```

---

## ✅ CHECKLIST DE VERIFICAÇÃO

Depois de configurar, verifique:

### No Streamlit Cloud:
- [ ] App está rodando
- [ ] Chatbot carregou
- [ ] Status mostra "IA Real Ativa"
- [ ] Perguntas respondem com IA

### No Codespace:
- [ ] Terminal mostra "DeepSeek API configurada"
- [ ] Dashboard carregou sem erros
- [ ] Chatbot funciona

### No Local:
- [ ] Arquivo `.env` existe
- [ ] Contém chave válida (sk-...)
- [ ] Dashboard roda sem erros

---

## 🐛 TROUBLESHOOTING

### Problema: "Modo Simulado" sempre ativo

**Possíveis Causas:**

1. **Chave não configurada:**
   - Verifique se secret foi salvo
   - Verifique se nome está correto: `deepseek` (não `DEEPSEEK`)

2. **Formato incorreto:**
   - Deve ser formato TOML (veja template acima)
   - Indentação importa!

3. **App não reiniciou:**
   - No Streamlit Cloud: Clique em "⋮" → "Reboot app"
   - No Codespace: Pare e inicie novamente

### Problema: "API Error"

**Possíveis Causas:**

1. **Chave inválida/expirada:**
   - Gere nova chave no DeepSeek
   - Atualize o secret

2. **Sem créditos:**
   - Verifique saldo em https://platform.deepseek.com

3. **Rate limit:**
   - Aguarde alguns minutos
   - Chatbot automaticamente usa fallback

---

## 📞 ONDE ENCONTRAR CADA PAINEL

### Streamlit Cloud Secrets:
```
https://share.streamlit.io/ → [Seu App] → ⋮ → Settings → Secrets
```

### GitHub Codespaces Secrets:
```
https://github.com/[usuario]/[repo] → Settings → Secrets and variables → Codespaces
```

### GitHub Actions Secrets:
```
https://github.com/[usuario]/[repo] → Settings → Secrets and variables → Actions
```

---

## 🎓 BOAS PRÁTICAS

### ✅ FAÇA:
- Use secrets do ambiente de deploy
- Revogue chaves antigas ao criar novas
- Monitore uso da API
- Use chaves diferentes por ambiente (dev/prod)

### ❌ NÃO FAÇA:
- Commitar `.env` no Git
- Compartilhar chaves por WhatsApp/SMS
- Usar mesma chave em produção e dev
- Deixar chaves em logs ou screenshots

---

## 🔗 LINKS ÚTEIS

- **DeepSeek Platform:** https://platform.deepseek.com
- **Streamlit Cloud:** https://share.streamlit.io
- **GitHub Secrets Docs:** https://docs.github.com/en/actions/security-guides/encrypted-secrets
- **Streamlit Secrets Docs:** https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/secrets-management

---

## 🎉 RESUMO

✅ **3 maneiras de configurar secrets:**
1. Streamlit Cloud → Para deploy público
2. GitHub Codespaces → Para desenvolvimento na nuvem
3. Arquivo .env → Para desenvolvimento local

✅ **Código funciona em todos os ambientes automaticamente**

✅ **Chave API nunca fica exposta no código**

---

**🔐 Sua chave está segura!**

Agora você pode fazer deploy do dashboard sem expor credenciais! 🚀
