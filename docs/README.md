# Rastreador de Gestos com Macaco

Sistema de reconhecimento de gestos em tempo real desenvolvido em Python que utiliza visão computacional para detectar movimentos das mãos através da câmera e exibe imagens correspondentes aos gestos detectados.

## Índice

- [Visão Geral](#visão-geral)
- [Funcionalidades](#funcionalidades)
- [Requisitos do Sistema](#requisitos-do-sistema)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Uso](#uso)
- [Arquitetura](#arquitetura)
- [Gestos Suportados](#gestos-suportados)
- [Personalização](#personalização)
- [Solução de Problemas](#solução-de-problemas)
- [Contribuindo](#contribuindo)
- [Licença](#licença)

---

## Visão Geral

Este projeto implementa um sistema de rastreamento e reconhecimento de gestos das mãos utilizando técnicas modernas de visão computacional e aprendizado de máquina. O sistema captura vídeo em tempo real, processa os frames para detectar landmarks das mãos, identifica gestos específicos e fornece feedback visual através de imagens correlatas.

### Tecnologias Utilizadas

- **OpenCV**: Processamento de imagens e captura de vídeo
- **MediaPipe**: Framework do Google para detecção e rastreamento de mãos
- **NumPy**: Operações matemáticas e manipulação de arrays

---

## Funcionalidades

- Detecção de gestos em tempo real com baixa latência
- Reconhecimento de múltiplos gestos pré-definidos:
  - **Neutro**: Posição de repouso/padrão
  - **Dedo no canto da boca**: Indicador próximo à região facial
  - **Dedo indicador para cima**: Indicador apontando verticalmente
  - **Mão no peito**: Mão aberta posicionada na região torácica
- Rastreamento de 21 landmarks por mão detectada
- Suporte para múltiplas câmeras
- Interface visual com overlay de imagens
- Sistema de feedback em tempo real

---

## Requisitos do Sistema

---

## Requisitos do Sistema

### Software

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Webcam funcional conectada ao computador

### Sistemas Operacionais Suportados

- Windows 10/11
- macOS 10.14 ou superior
- Linux (Ubuntu 18.04+, Debian, Fedora)

### Dependências Python

```
opencv-python >= 4.8.0
mediapipe >= 0.10.0
numpy >= 1.24.0
```

---

## Instalação

### 1. Clone o Repositório

```bash
git clone <url-do-repositorio>
cd monkey
```

### 2. Crie um Ambiente Virtual (Recomendado)

```bash
# No Windows
python -m venv venv
venv\Scripts\activate

# No macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as Dependências

#### Opção A: Via requirements.txt (Recomendado)

```bash
pip install -r requirements.txt
```

#### Opção B: Instalação Manual

```bash
pip install opencv-python mediapipe numpy
```

### 4. Verifique a Instalação

```bash
python -c "import cv2, mediapipe, numpy; print('Instalação bem-sucedida!')"
```

---

## Configuração

---

## Configuração

### Estrutura de Diretórios

```
monkey/
├── gesture_tracker.py      # Arquivo principal
├── requirements.txt         # Dependências
├── monkey_images/          # Pasta de recursos visuais
│   ├── neutral.png
│   ├── finger_mouth.png
│   ├── finger_up.png
│   └── hand_chest.png
└── docs/
    └── README.md
```

### Preparação dos Recursos Visuais

Antes de executar o programa, é necessário adicionar imagens correspondentes aos gestos na pasta `monkey_images/`:

#### Arquivos Necessários

| Arquivo            | Descrição                         | Especificações             |
| ------------------ | --------------------------------- | -------------------------- |
| `neutral.png`      | Imagem padrão (posição neutra)    | PNG, 300x300px recomendado |
| `finger_mouth.png` | Gesto de dedo no canto da boca    | PNG, 300x300px recomendado |
| `finger_up.png`    | Gesto de dedo indicador para cima | PNG, 300x300px recomendado |
| `hand_chest.png`   | Gesto de mão no peito             | PNG, 300x300px recomendado |

#### Obtenção de Imagens

**Opção 1: Bancos de Imagens Gratuitos**

- [Unsplash](https://unsplash.com) - Imagens de alta qualidade
- [Pexels](https://pexels.com) - Fotografias e vídeos gratuitos
- [Pixabay](https://pixabay.com) - Recursos visuais livres

**Opção 2: Geração por IA**

- DALL-E, Midjourney, Stable Diffusion
- Prompts sugeridos: "cartoon monkey [gesture] pose", "cute monkey [gesture]"

**Opção 3: Design Personalizado**

- Crie suas próprias ilustrações
- Use ferramentas de edição gráfica (GIMP, Photoshop, Canva)

#### Notas Importantes

- Os nomes dos arquivos devem ser **exatamente** como especificado
- Formato PNG é recomendado para suporte a transparência
- Imagens com fundo transparente proporcionam melhor resultado visual
- Resolução recomendada: 300x300 pixels (redimensionamento automático aplicado)

---

## Uso

### Execução Básica

```bash
python gesture_tracker.py
```

### Fluxo de Execução

1. **Inicialização**: O programa detecta câmeras disponíveis
2. **Seleção de Câmera**: Se múltiplas câmeras estiverem disponíveis, selecione a desejada
3. **Detecção de Gestos**: Posicione a mão em frente à câmera
4. **Feedback Visual**: A imagem correspondente ao gesto será exibida
5. **Encerramento**: Pressione 'q' para sair

### Controles

| Tecla | Ação                |
| ----- | ------------------- |
| `q`   | Encerrar o programa |

### Exemplo de Sessão

```
============================================================
RASTREADOR DE GESTOS COM MACACO
============================================================
Sistema de reconhecimento de gestos em tempo real
Desenvolvido com OpenCV e MediaPipe
============================================================

Procurando câmeras disponíveis...

Câmeras disponíveis: [0, 1]

Escolha a câmera [0, 1] (padrão: 0): 0

============================================================
CÂMERA INICIADA!
============================================================
Usando câmera: 0

GESTOS DISPONÍVEIS:
   Dedo indicador para cima
   Dedo no canto da boca
   Mão no peito
   Neutro (sem gesto específico)

Pressione 'q' para sair
============================================================
```

---

## Arquitetura

---

## Arquitetura

### Visão Geral do Sistema

```
┌─────────────────┐
│   Câmera USB    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  OpenCV Capture │ ◄── Captura de frames em tempo real
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ MediaPipe Hands │ ◄── Detecção de 21 landmarks por mão
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Gesture Analyzer│ ◄── Análise de padrões e classificação
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Image Overlay  │ ◄── Sobreposição de imagens
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Display GUI   │ ◄── Exibição do resultado
└─────────────────┘
```

### Componentes Principais

#### 1. GestureTracker (Classe Principal)

Gerencia todo o pipeline de detecção e reconhecimento de gestos.

**Responsabilidades:**

- Inicialização do MediaPipe e OpenCV
- Gerenciamento de recursos (imagens, câmera)
- Coordenação do fluxo de processamento

#### 2. Sistema de Detecção de Mãos

Utiliza o MediaPipe Hands para identificar e rastrear landmarks das mãos.

**Características:**

- Detecção de até 2 mãos simultaneamente
- 21 landmarks 3D por mão
- Confiança mínima configurável (padrão: 50%)

#### 3. Algoritmo de Reconhecimento de Gestos

Analisa os landmarks para identificar padrões específicos.

**Metodologia:**

- Análise de dedos levantados/abaixados
- Cálculo de distâncias entre landmarks
- Verificação de posições relativas
- Aplicação de regras heurísticas

#### 4. Sistema de Overlay

Sobrepõe imagens com suporte a transparência (canal alpha).

**Funcionalidades:**

- Carregamento dinâmico de imagens
- Redimensionamento automático
- Blending com canal alpha
- Posicionamento configurável

---

## Gestos Suportados

### 1. Neutro (neutral)

**Descrição**: Estado padrão quando nenhum gesto específico é detectado.

**Critérios de Detecção**: Ativado por exclusão quando nenhum outro padrão é identificado.

### 2. Dedo no Canto da Boca (finger_mouth)

**Descrição**: Indicador próximo à região facial lateral.

**Critérios de Detecção**:

- Indicador levantado
- Mão posicionada na parte superior da imagem (Y < 0.6)
- Distância vertical indicador-pulso < 0.4
- Máximo 2 dedos levantados

**Uso Típico**: Gesto pensativo ou questionador.

### 3. Dedo Indicador Para Cima (finger_up)

**Descrição**: Indicador apontando verticalmente para cima.

**Critérios de Detecção**:

- Apenas o indicador levantado (outros dedos fechados)
- Ponta do indicador significativamente acima do pulso (Y < pulso.Y - 0.2)

**Uso Típico**: Apontar, chamar atenção, número 1.

### 4. Mão no Peito (hand_chest)

**Descrição**: Mão aberta posicionada na região torácica central.

**Critérios de Detecção**:

- Centro da mão na parte inferior da imagem (Y > 0.6)
- Posição horizontal centralizada (|X - 0.5| < 0.3)
- Mínimo de 3 dedos visíveis

**Uso Típico**: Gesto de compromisso, sinceridade, autorreferência.

---

## Personalização

### Adicionar Novos Gestos

#### Passo 1: Definir a Lógica de Detecção

---

## Personalização

### Adicionar Novos Gestos

#### Passo 1: Definir a Lógica de Detecção

Edite o método `detect_gesture()` em `gesture_tracker.py`:

```python
def detect_gesture(self, hand_landmarks, handedness):
    fingers = self.count_fingers(hand_landmarks, handedness)
    fingers_count = sum(fingers)

    # Exemplo: Detectar sinal de "OK"
    thumb_tip = hand_landmarks[4]
    index_tip = hand_landmarks[8]
    distance = math.sqrt(
        (thumb_tip.x - index_tip.x)**2 +
        (thumb_tip.y - index_tip.y)**2
    )

    if distance < 0.05 and fingers_count >= 3:
        return "ok_sign"

    # ... resto da lógica
```

#### Passo 2: Adicionar Recurso Visual

1. Adicione o mapeamento em `load_monkey_images()`:

```python
gesture_files = {
    "neutral": "neutral.png",
    "finger_mouth": "finger_mouth.png",
    "finger_up": "finger_up.png",
    "hand_chest": "hand_chest.png",
    "ok_sign": "ok_sign.png"  # Novo gesto
}
```

2. Crie/adicione o arquivo `ok_sign.png` na pasta `monkey_images/`

#### Passo 3: Testar e Ajustar

Execute o programa e ajuste os parâmetros de detecção conforme necessário para melhorar a precisão.

### Configurar Parâmetros de Detecção

Ajuste a sensibilidade do MediaPipe no método `__init__()`:

```python
self.hands = self.mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,                    # Número máximo de mãos
    min_detection_confidence=0.7,       # Aumentar para maior precisão
    min_tracking_confidence=0.7         # Aumentar para rastreamento mais estável
)
```

### Personalizar Interface Visual

**Alterar posição do overlay:**

```python
# No método run()
x_offset = image.shape[1] - 320  # Distância da borda direita
y_offset = 10                     # Distância do topo
```

**Alterar tamanho das imagens:**

```python
# No método load_monkey_images()
img = cv2.resize(img, (400, 400))  # Tamanho personalizado
```

---

## Solução de Problemas

### Problemas Comuns e Soluções

---

## Solução de Problemas

### Problemas Comuns e Soluções

#### Câmera não inicializa

**Sintomas**: Erro "Não foi possível abrir a câmera" ou programa não exibe vídeo.

**Soluções**:

1. Verificar se a câmera está conectada e funcionando
2. Fechar outros aplicativos que possam estar usando a câmera (Zoom, Skype, etc.)
3. No macOS: Conceder permissões de câmera ao Terminal
   - `System Preferences > Security & Privacy > Camera`
4. No Linux: Verificar permissões de dispositivo
   ```bash
   ls -l /dev/video*
   sudo usermod -a -G video $USER
   ```

#### Gestos não são reconhecidos adequadamente

**Sintomas**: Sistema não detecta gestos ou detecta incorretamente.

**Soluções**:

1. **Iluminação**: Garantir iluminação adequada e uniforme
   - Evitar contraluz
   - Usar luz frontal ou lateral
2. **Posicionamento**:
   - Manter a mão a 30-60cm da câmera
   - Garantir que toda a mão esteja visível
   - Evitar movimentos muito rápidos
3. **Fundo**:
   - Usar fundo neutro e uniforme
   - Evitar cores similares à pele
   - Minimizar movimento no fundo
4. **Ajuste de Sensibilidade**:
   - Aumentar `min_detection_confidence` para reduzir falsos positivos
   - Diminuir para detecção mais sensível

#### Imagens do macaco não aparecem

**Sintomas**: Gestos detectados mas sem overlay visual.

**Soluções**:

1. Verificar estrutura de diretórios:
   ```bash
   ls monkey_images/
   ```
2. Confirmar nomes exatos dos arquivos (case-sensitive)
3. Verificar formato dos arquivos (PNG recomendado)
4. Verificar logs de inicialização para mensagens de erro
5. Confirmar que as imagens não estão corrompidas:
   ```python
   import cv2
   img = cv2.imread('monkey_images/neutral.png')
   print(img is not None)  # Deve retornar True
   ```

#### Performance/Lag

**Sintomas**: Processamento lento, frames cortados, atraso.

**Soluções**:

1. Reduzir resolução da câmera:
   ```python
   cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
   cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
   ```
2. Reduzir número máximo de mãos detectadas:
   ```python
   max_num_hands=1
   ```
3. Aumentar intervalo de processamento:
   ```python
   if cv2.waitKey(10) & 0xFF == ord('q'):  # 5 -> 10
   ```
4. Fechar outros programas consumindo recursos

#### Erros de Dependências

**Sintomas**: Erros de importação ou incompatibilidade de versões.

**Soluções**:

1. Reinstalar dependências:
   ```bash
   pip uninstall opencv-python mediapipe numpy
   pip install -r requirements.txt
   ```
2. Criar ambiente virtual limpo:
   ```bash
   python -m venv venv_new
   source venv_new/bin/activate  # Linux/Mac
   pip install -r requirements.txt
   ```
3. Verificar versão do Python:
   ```bash
   python --version  # Deve ser >= 3.8
   ```

### Logs e Debugging

Para habilitar logs detalhados, modifique o código:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# No método detect_gesture()
print(f"Dedos: {fingers}, Count: {fingers_count}")
print(f"Index Y: {index_tip.y}, Wrist Y: {wrist.y}")
```

---

## Contribuindo

Contribuições são bem-vindas! Para contribuir:

### Processo de Contribuição

1. **Fork** o repositório
2. **Crie** uma branch para sua feature (`git checkout -b feature/NovaFuncionalidade`)
3. **Commit** suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. **Push** para a branch (`git push origin feature/NovaFuncionalidade`)
5. **Abra** um Pull Request

### Diretrizes

- Mantenha o código limpo e bem documentado
- Adicione docstrings para novos métodos/funções
- Siga as convenções PEP 8 de estilo Python
- Teste suas alterações antes de submeter
- Atualize a documentação conforme necessário

### Áreas de Melhoria

- Adicionar novos gestos
- Melhorar algoritmos de detecção
- Otimizar performance
- Adicionar suporte a configuração via arquivo
- Implementar gravação de sessões
- Criar interface gráfica (GUI)
- Adicionar testes unitários
- Internacionalização (i18n)

---

## Licença

Este projeto é distribuído sob licença de código aberto. Sinta-se livre para modificar e utilizar conforme necessário.

---

## Autores e Reconhecimentos

**Desenvolvido por**: Sistema de Rastreamento de Gestos

**Agradecimentos**:

- Google MediaPipe Team pela biblioteca de detecção de mãos
- Comunidade OpenCV pelo framework de visão computacional
- Contribuidores e testadores do projeto

---

## Contato e Suporte

Para questões, sugestões ou reportar bugs:

- Abra uma issue no repositório
- Consulte a documentação técnica
- Revise a seção de Solução de Problemas

---

**Versão**: 1.0.0  
**Última Atualização**: Novembro 2025  
**Status**: Ativo
