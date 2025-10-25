# 🔒 CONFIGURAÇÃO SEGURA DO CHATBOT

## ⚠️ IMPORTANTE: SEGURANÇA DA CHAVE API

O chatbot usa a API do DeepSeek, que requer uma chave secreta. **NUNCA commite sua chave API no Git!**

---

## ✅ ARQUIVOS DE SEGURANÇA

### Estrutura de Arquivos:

```
Business/
├── .env                 ❌ NUNCA COMMITAR (sua chave real está aqui)
├── .env.example         ✅ COMMITAR (template sem chave)
├── .gitignore           ✅ COMMITAR (bloqueia .env)
└── ai_chatbot.py        ✅ COMMITAR (código do chatbot)
```

### O que cada arquivo faz:

| Arquivo | Contém | Commitar? | Descrição |
|---------|--------|-----------|-----------|
| `.env` | Chave API REAL | ❌ NÃO | Sua chave secreta |
| `.env.example` | Template | ✅ SIM | Exemplo para equipe |
| `.gitignore` | Regras | ✅ SIM | Protege arquivos sensíveis |

---

## 🚀 CONFIGURAÇÃO PARA NOVOS USUÁRIOS

### Se você clonou o repositório:

1. **Copie o arquivo de exemplo:**
   ```bash
   cp .env.example .env
   ```

2. **Obtenha sua chave DeepSeek:**
   - Acesse: https://platform.deepseek.com
   - Crie conta / Faça login
   - Vá em "API Keys" → "Create API Key"
   - Copie a chave (começa com `sk-`)

3. **Edite o arquivo .env:**
   ```bash
   # Abra com qualquer editor
   notepad .env
   # ou
   code .env
   ```

4. **Cole sua chave:**
   ```
   DEEPSEEK_API_KEY=sk-sua_chave_aqui_xxxxxxxxxx
   ```

5. **Salve e rode o dashboard:**
   ```bash
   streamlit run main.py
   ```

---

## 🔐 VERIFICAÇÃO DE SEGURANÇA

### Antes de commitar, SEMPRE verifique:

```bash
# ✅ Verificar se .env está no .gitignore
cat .gitignore | grep ".env"

# ✅ Verificar se .env NÃO está no Git
git status

# ✅ Verificar o que será commitado
git diff --cached

# ❌ Se você ver sua chave no output, PARE!
```

---

## ⚡ COMANDOS SEGUROS PARA COMMITAR

### Passo a Passo Seguro:

```bash
# 1. Ver status atual
git status

# 2. Adicionar apenas arquivos necessários (SEM .env)
git add .gitignore
git add .env.example
git add ai_chatbot.py
git add main.py
git add CONFIGURACAO_SEGURA.md

# 3. Verificar o que será commitado
git status

# 4. Se estiver tudo OK, commitar
git commit -m "Chatbot integrado com DeepSeek (sem chave API)"

# 5. Push para GitHub
git push origin master
```

### Ou, se tiver certeza que .gitignore está correto:

```bash
# Adicionar todos exceto os ignorados
git add .

# Verificar (NÃO deve listar .env)
git status

# Commitar e push
git commit -m "Chatbot integrado com DeepSeek"
git push
```

---

## 🆘 E SE EU JÁ COMMITEI A CHAVE?

### 😱 Acidentalmente commitou a chave API?

**AÇÃO IMEDIATA:**

1. **REVOGUE a chave imediatamente:**
   - Acesse: https://platform.deepseek.com/api_keys
   - Delete a chave comprometida
   - Gere uma nova

2. **Remova do histórico do Git:**
   ```bash
   # Remover arquivo do último commit
   git rm --cached .env
   git commit --amend -m "Remove .env acidentalmente commitado"
   git push -f
   ```

3. **Se já foi pushado há tempo:**
   ```bash
   # Considere reescrever o histórico (avançado)
   # Ou apenas revogue a chave e siga em frente
   ```

---

## 👥 COMPARTILHANDO COM A EQUIPE

### Opção 1: Cada um cria sua chave (Recomendado)

1. Compartilhe o repositório (sem .env)
2. Instrua a equipe a:
   - Copiar `.env.example` para `.env`
   - Criar conta DeepSeek
   - Obter própria chave
   - Configurar localmente

**Vantagens:**
- ✅ Mais seguro
- ✅ Rastreamento individual de uso
- ✅ Sem compartilhamento de credenciais

### Opção 2: Compartilhar uma chave (Menos seguro)

Se realmente necessário, compartilhe por **canal seguro**:

- ✅ Discord/Slack (mensagem direta)
- ✅ Email criptografado
- ✅ Gerenciador de senhas (1Password, LastPass)
- ❌ NUNCA por: WhatsApp, SMS, Git, código fonte

---

## 📊 VERIFICAR SE ESTÁ FUNCIONANDO

### Teste rápido:

1. **Abra o dashboard:**
   ```bash
   streamlit run main.py
   ```

2. **Vá no Chatbot**

3. **Abra "⚙️ Configurações Avançadas"**

4. **Verifique:**
   - ✅ "IA Real Ativa - DeepSeek" = Funcionando!
   - ⚠️ "Modo Simulado" = Chave não configurada

---

## 🎯 CHECKLIST FINAL

Antes de fazer push:

- [ ] Arquivo `.env` existe localmente
- [ ] Arquivo `.env.example` existe (sem chave real)
- [ ] Arquivo `.gitignore` contém `.env`
- [ ] Executei `git status` e `.env` NÃO aparece
- [ ] Chatbot funciona localmente
- [ ] Li esta documentação completamente

---

## 💡 DICAS EXTRAS

### Para administradores:

1. **Configure GitHub Secrets (para CI/CD):**
   - Settings → Secrets and variables → Actions
   - Adicione `DEEPSEEK_API_KEY`

2. **Use .env diferentes por ambiente:**
   - `.env.development`
   - `.env.production`
   - `.env.test`

3. **Monitore uso da API:**
   - https://platform.deepseek.com/usage
   - Configure alertas de custo

---

## 📞 SUPORTE

Se tiver dúvidas sobre segurança:

1. Leia: [12-Factor App - Config](https://12factor.net/config)
2. Leia: [OWASP - Credential Security](https://owasp.org/)
3. Consulte a equipe de TI

---

**🔒 Segurança é responsabilidade de todos!**
