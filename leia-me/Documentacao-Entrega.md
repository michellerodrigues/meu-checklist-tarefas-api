# Projeto MVP - Meu Checklist de Tarefas


A ideia surgiu das tarefas que tenho coladas na minha geladeira. A ideia é trazer esse board para o celular/web de forma intuitiva e agradável.

![image](https://github.com/user-attachments/assets/e1a1dc10-b70f-452d-b5fc-20f013514c9a)

## Apresentação Aplicativo

[MeuCheckLisTarefas-Apresentação.pptx](https://github.com/user-attachments/files/19722216/MeuCheckLisTarefas-Apresentacao.pptx)


## Visão Geral
A ideia dessa aplicação é oferecer ao usuário um painel com tarefas pré-cadastradas, de acordo com a necessidade de cada usuário.  
Baseado num contexto de gestão à vista, ter um painel com todas as tarefas frequentes do dia-a-dia traz facilidade e mais tranquilidade para organizar as demandas.  

O aplicativo vai mais longe, pois permitirá:
- Monetizar tarefas com membros da família
- Buscar profissionais para execução de tarefas específicas

**Foco principal**:  
✔ Usabilidade  
✔ Experiência do usuário (IHC)  
✔ Redução de _overwhelm_ (seleção automática de tarefas pré-definidas)  

---

## Fluxo Principal - MVP

1. **Cadastro**:  
   - Usuário acessa a página  
   - Realiza cadastro  
   - É direcionado para login  

2. **Primeiro Login**:  
   - Usuário responde questionário sobre estilo de vida  
   - *Débito técnico*:  
     - Versão atual usa `localStorage` para tags  
     - Próxima versão: implementar token JWT com claims  

3. **Questionário**:  
   - Todas as perguntas são obrigatórias  
   - Navegação livre (avançar/retroceder)  
   - Após envio:  
     - Painel é carregado com tarefas filtradas  
     - *Débito técnico*: Salvar estado de tarefas concluídas  

4. **Logins subsequentes**:  
   - Direto para o painel  
   - Tarefas filtradas pelas tags do questionário  

---

## Funcionalidades Entregues no MVP

### Frontend & Backend
✅ Login de usuário  
✅ Cadastro de usuário  
✅ Questionário com tags personalizadas  
✅ Listagem de tarefas por perfil  

---

## Roadmap

### Versão Gratuita (Futuro)
| Funcionalidade | Descrição |
|----------------|-----------|
| Histórico de tarefas | Data da última execução |
| Alertas de atraso | Ex: tarefa semanal > 2 semanas |
| Família | Cadastro e compartilhamento de painel |
| Monetização | Atribuir valor às tarefas |

### Versão Paga (Futuro)
🔧 **Edição avançada**:  
- Alterar frequência de tarefas  
- Adicionar/remover tarefas/categorias  

💸 **Integrações**:  
- Pagamento de tarefas monetizadas  
- Contato direto com profissionais  

---

## Débitos Técnicos
- [ ] Implementar autenticação via token JWT  
- [ ] Persistência de estado de tarefas concluídas  
- [ ] Sistema de notificações (e-mail/SMS)  
