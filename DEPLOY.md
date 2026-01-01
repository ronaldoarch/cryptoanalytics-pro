# 🚀 Guia de Deploy - Railway

Este guia explica como fazer deploy do CryptoAnalytics Pro no Railway.

## Pré-requisitos

- Conta no [Railway](https://railway.app)
- Repositório no GitHub (já configurado)

## Passo a Passo

### 1. Conectar Railway ao GitHub

1. Acesse [railway.app](https://railway.app)
2. Faça login com sua conta GitHub
3. Clique em **"New Project"**
4. Selecione **"Deploy from GitHub repo"**
5. Escolha o repositório `cryptoanalytics-pro`
6. Railway irá detectar automaticamente o projeto Python

### 2. Configuração Automática

O Railway detectará automaticamente:
- ✅ `requirements.txt` - Dependências Python
- ✅ `Procfile` - Comando de inicialização
- ✅ `railway.json` - Configurações do Railway
- ✅ Porta via variável `PORT` (configurada automaticamente)

### 3. Variáveis de Ambiente (Opcional)

Se necessário, você pode adicionar variáveis de ambiente no Railway:

1. Vá em **Settings** → **Variables**
2. Adicione variáveis se necessário:
   - `ENVIRONMENT=production` (opcional)
   - `PORT` (já configurado automaticamente pelo Railway)

### 4. Deploy

1. O Railway iniciará o build automaticamente
2. Aguarde o build completar
3. O deploy será feito automaticamente
4. Railway fornecerá uma URL pública (ex: `https://cryptoanalytics-pro.up.railway.app`)

### 5. Verificar Deploy

Após o deploy, teste os endpoints:

- **Dashboard**: `https://seu-projeto.up.railway.app/`
- **API Docs**: `https://seu-projeto.up.railway.app/docs`
- **Health Check**: `https://seu-projeto.up.railway.app/health`

## Arquivos de Configuração

### Procfile
```
web: python main.py
```
Define o comando para iniciar a aplicação.

### railway.json
```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python main.py",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### main.py
Já configurado para:
- ✅ Usar porta da variável `PORT` (Railway fornece automaticamente)
- ✅ Detectar ambiente de produção
- ✅ Desabilitar reload em produção

## Troubleshooting

### Build Falha

1. Verifique os logs no Railway
2. Confirme que `requirements.txt` está correto
3. Verifique se todas as dependências são compatíveis

### Aplicação não inicia

1. Verifique os logs: **Deployments** → **View Logs**
2. Confirme que a porta está sendo lida corretamente
3. Verifique se não há erros de importação

### Erro 502 Bad Gateway

1. Verifique se a aplicação está rodando
2. Confirme que está escutando em `0.0.0.0` (já configurado)
3. Verifique os logs de erro

## Atualizações Futuras

Para atualizar o deploy:

1. Faça commit das mudanças no GitHub
2. Railway detectará automaticamente e fará novo deploy
3. Ou clique em **"Redeploy"** no Railway

## Domínio Customizado (Opcional)

1. Vá em **Settings** → **Domains**
2. Adicione seu domínio customizado
3. Configure DNS conforme instruções do Railway

## Monitoramento

Railway fornece:
- ✅ Logs em tempo real
- ✅ Métricas de uso
- ✅ Histórico de deploys
- ✅ Status do serviço

## Custos

- Railway oferece plano gratuito generoso
- Verifique limites em [railway.app/pricing](https://railway.app/pricing)

## Alternativas de Deploy

Se preferir outras plataformas:

- **Heroku**: Similar ao Railway
- **Render**: Outra opção popular
- **Fly.io**: Boa para aplicações Python
- **AWS/GCP**: Para produção em escala

---

**Pronto!** Seu projeto estará online em minutos! 🎉

