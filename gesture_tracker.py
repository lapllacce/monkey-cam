#!/usr/bin/env python3
"""
====================================================================
    RASTREADOR DE GESTOS COM MACACO
====================================================================

Descrição:
    Sistema de reconhecimento de gestos em tempo real que detecta
    movimentos específicos das mãos usando a câmera e exibe imagens
    de um macaco realizando o mesmo gesto.

Gestos Reconhecidos:
    1. Neutro - Posição padrão/repouso
    2. Dedo no canto da boca - Indicador próximo ao rosto
    3. Dedo indicador para cima - Indicador apontando para cima
    4. Mão no peito - Mão aberta na região do peito

Tecnologias:
    - OpenCV: Captura e processamento de vídeo
    - MediaPipe: Detecção e rastreamento de mãos
    - NumPy: Operações matemáticas

Autor: Sistema de Rastreamento de Gestos
Data: 2025
====================================================================
"""

import math
# ============================================================
# IMPORTAÇÕES
# ============================================================
import os

import cv2
import mediapipe as mp
import numpy as np


# ============================================================
# CLASSE PRINCIPAL: GestureTracker
# ============================================================
class GestureTracker:
    """
    Classe responsável pelo rastreamento e reconhecimento de gestos.
    
    Atributos:
        mp_hands: Módulo de detecção de mãos do MediaPipe
        mp_drawing: Utilitários de desenho do MediaPipe
        mp_drawing_styles: Estilos de desenho do MediaPipe
        hands: Instância do detector de mãos
        monkey_images: Dicionário com as imagens dos gestos do macaco
        current_gesture: Gesto atualmente detectado
    """
    
    def __init__(self):
        """Inicializa o rastreador de gestos e carrega os recursos necessários."""
        
        # ========================================
        # Inicialização do MediaPipe
        # ========================================
        self.mp_hands = mp.solutions.hands  # type: ignore
        self.mp_drawing = mp.solutions.drawing_utils  # type: ignore
        self.mp_drawing_styles = mp.solutions.drawing_styles  # type: ignore
        
        # ========================================
        # Configuração do Detector de Mãos
        # ========================================
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,        # False = modo de vídeo (mais rápido)
            max_num_hands=2,                # Detecta até 2 mãos simultaneamente
            min_detection_confidence=0.5,   # Confiança mínima para detecção (0-1)
            min_tracking_confidence=0.5     # Confiança mínima para rastreamento (0-1)
        )
        
        # ========================================
        # Recursos do Sistema
        # ========================================
        self.monkey_images = self.load_monkey_images()  # Carrega imagens dos gestos
        self.current_gesture = "neutral"                 # Gesto inicial: neutro
        
    # ========================================
    # MÉTODO: Carregar Imagens
    # ========================================
    def load_monkey_images(self):
        """
        Carrega as imagens dos gestos do macaco da pasta 'monkey_images/'.
        
        Returns:
            dict: Dicionário com {nome_do_gesto: imagem_carregada}
        """
        images = {}
        image_dir = "monkey_images"
        
        # Verificar se o diretório existe
        if not os.path.exists(image_dir):
            os.makedirs(image_dir)
            print(f"📁 Criado diretório {image_dir}")
            print("⚠️  Adicione imagens de macacos nesta pasta:")
            print("   - neutral.png (posição neutra)")
            print("   - finger_mouth.png (dedo no canto da boca)")
            print("   - finger_up.png (dedo indicador para cima)")
            print("   - hand_chest.png (mão no peito)")
        
        # Mapeamento dos gestos e seus arquivos
        gesture_files = {
            "neutral": "neutral.png",
            "finger_mouth": "finger_mouth.png",
            "finger_up": "finger_up.png",
            "hand_chest": "hand_chest.png"
        }
        
        # Carregar cada imagem
        for gesture, filename in gesture_files.items():
            filepath = os.path.join(image_dir, filename)
            
            if os.path.exists(filepath):
                # Ler imagem (IMREAD_UNCHANGED preserva canal alpha/transparência)
                img = cv2.imread(filepath, cv2.IMREAD_UNCHANGED)
                
                if img is not None:
                    # Redimensionar para tamanho padrão (300x300 pixels)
                    img = cv2.resize(img, (300, 300))
                    images[gesture] = img
                    print(f"✅ Carregada: {filename}")
                else:
                    print(f"❌ Erro ao ler: {filename}")
            else:
                print(f"⚠️  Não encontrada: {filename}")
        
        return images
    
    # ========================================
    # MÉTODO: Contar Dedos Levantados
    # ========================================
    def count_fingers(self, hand_landmarks, handedness):
        """
        Conta quantos dedos estão levantados com base nos landmarks da mão.
        
        Args:
            hand_landmarks: Lista de landmarks (21 pontos) da mão
            handedness: "Right" ou "Left" (mão direita ou esquerda)
        
        Returns:
            list: Lista de 5 elementos [polegar, indicador, médio, anelar, mínimo]
                  onde 1 = levantado e 0 = abaixado
        
        Nota:
            O MediaPipe detecta 21 landmarks por mão:
            - 0: Pulso
            - 4, 8, 12, 16, 20: Pontas dos dedos
            - 3, 6, 10, 14, 18: Articulações médias
        """
        fingers_up = []
        
        # IDs dos landmarks importantes
        finger_tips = [4, 8, 12, 16, 20]    # Pontas dos 5 dedos
        finger_pips = [3, 6, 10, 14, 18]    # Articulações para comparação
        
        # ========================================
        # POLEGAR (lógica horizontal)
        # ========================================
        # O polegar se move horizontalmente, então comparamos coordenadas X
        if handedness == "Right":
            # Mão direita: polegar levantado = ponta mais à esquerda que articulação
            if hand_landmarks[finger_tips[0]].x < hand_landmarks[finger_pips[0]].x:
                fingers_up.append(1)
            else:
                fingers_up.append(0)
        else:  # Left
            # Mão esquerda: polegar levantado = ponta mais à direita que articulação
            if hand_landmarks[finger_tips[0]].x > hand_landmarks[finger_pips[0]].x:
                fingers_up.append(1)
            else:
                fingers_up.append(0)
        
        # ========================================
        # OUTROS DEDOS (lógica vertical)
        # ========================================
        # Os outros dedos se movem verticalmente, então comparamos coordenadas Y
        for i in range(1, 5):
            # Dedo levantado = ponta (Y menor) acima da articulação (Y maior)
            # Nota: No OpenCV, Y cresce de cima para baixo
            if hand_landmarks[finger_tips[i]].y < hand_landmarks[finger_pips[i]].y:
                fingers_up.append(1)  # Levantado
            else:
                fingers_up.append(0)  # Abaixado
        
        return fingers_up
    
    # ========================================
    # MÉTODO: Detectar Gesto
    # ========================================
    def detect_gesture(self, hand_landmarks, handedness):
        """
        Identifica o gesto que está sendo realizado.
        
        Args:
            hand_landmarks: Lista de 21 landmarks da mão
            handedness: "Right" ou "Left"
        
        Returns:
            str: Nome do gesto detectado ("finger_mouth", "finger_up", 
                 "hand_chest", ou "neutral")
        
        Lógica de Detecção:
            - Analisa quais dedos estão levantados
            - Calcula posições e distâncias entre landmarks
            - Aplica regras específicas para cada gesto
        """
        # Obter estado dos dedos (quais estão levantados)
        fingers = self.count_fingers(hand_landmarks, handedness)
        fingers_count = sum(fingers)  # Total de dedos levantados
        
        # fingers = [polegar, indicador, médio, anelar, mínimo]
        # Exemplo: [0, 1, 0, 0, 0] = apenas indicador levantado
        
        # ========================================
        # Extrair Landmarks Importantes
        # ========================================
        wrist = hand_landmarks[0]          # Pulso (base da mão)
        thumb_tip = hand_landmarks[4]      # Ponta do polegar
        index_tip = hand_landmarks[8]      # Ponta do indicador
        index_pip = hand_landmarks[6]      # Articulação do indicador
        middle_tip = hand_landmarks[12]    # Ponta do dedo médio
        
        # ========================================
        # GESTO 1: Dedo no Canto da Boca
        # ========================================
        # Condições:
        #   - Indicador levantado
        #   - Mão próxima ao rosto (parte superior da tela)
        #   - Mão não está muito esticada
        #   - Poucos dedos levantados (1 ou 2)
        
        dist_index_wrist_y = abs(index_tip.y - wrist.y)  # Distância vertical
        
        if (fingers[1] == 1 and                    # Indicador levantado
            index_tip.y < 0.6 and                  # Parte superior/média (Y < 0.6)
            dist_index_wrist_y < 0.4 and           # Mão não muito esticada
            fingers_count <= 2):                   # Máximo 2 dedos levantados
            return "finger_mouth"
        
        # ========================================
        # GESTO 2: Dedo Indicador Para Cima
        # ========================================
        # Condições:
        #   - Apenas indicador levantado
        #   - Indicador apontando para cima (acima do pulso)
        
        if (fingers == [0, 1, 0, 0, 0] and         # Só indicador levantado
            index_tip.y < wrist.y - 0.2):          # Bem acima do pulso
            return "finger_up"
        
        # ========================================
        # GESTO 3: Mão no Peito
        # ========================================
        # Condições:
        #   - Mão na parte inferior da tela (região do peito)
        #   - Mão centralizada horizontalmente
        #   - Vários dedos visíveis (mão aberta/plana)
        
        # Calcular posição média/centro da mão
        hand_center_x = sum([hand_landmarks[i].x for i in [0, 5, 9, 13, 17]]) / 5
        hand_center_y = sum([hand_landmarks[i].y for i in [0, 5, 9, 13, 17]]) / 5
        
        chest_region_y = 0.6      # Região do peito (parte inferior, Y > 0.6)
        chest_region_x = 0.5      # Centro horizontal (X ≈ 0.5)
        
        if (hand_center_y > chest_region_y and              # Parte inferior
            abs(hand_center_x - chest_region_x) < 0.3 and   # Próximo ao centro
            fingers_count >= 3):                            # Pelo menos 3 dedos
            return "hand_chest"
        
        # ========================================
        # GESTO PADRÃO: Neutro
        # ========================================
        # Retorna se nenhum gesto específico for detectado
        return "neutral"
    
    # ========================================
    # MÉTODO: Sobrepor Imagem
    # ========================================
    def overlay_image(self, background, overlay, x, y):
        """
        Sobrepõe uma imagem (overlay) sobre outra (background) com suporte a transparência.
        
        Args:
            background: Imagem de fundo (frame da câmera)
            overlay: Imagem a ser sobreposta (imagem do macaco)
            x: Posição X (horizontal) onde colocar a imagem
            y: Posição Y (vertical) onde colocar a imagem
        
        Returns:
            numpy.ndarray: Imagem de fundo com overlay aplicado
        
        Nota:
            Suporta imagens PNG com canal alpha (transparência)
        """
        if overlay is None:
            return background
        
        h, w = overlay.shape[:2]  # Altura e largura do overlay
        
        # ========================================
        # Ajustar Tamanho se Não Couber na Tela
        # ========================================
        if x + w > background.shape[1]:
            w = background.shape[1] - x
            overlay = cv2.resize(overlay, (w, h))
        
        if y + h > background.shape[0]:
            h = background.shape[0] - y
            overlay = cv2.resize(overlay, (w, h))
        
        # Verificar se posição é válida
        if x < 0 or y < 0:
            return background
        
        # ========================================
        # Aplicar Transparência (Canal Alpha)
        # ========================================
        if overlay.shape[2] == 4:  # Imagem tem canal alpha (RGBA)
            # Normalizar alpha de 0-255 para 0-1
            alpha = overlay[:, :, 3] / 255.0
            
            # Misturar cada canal de cor (B, G, R)
            for c in range(3):
                background[y:y+h, x:x+w, c] = (
                    alpha * overlay[:, :, c] +                    # Parte visível do overlay
                    (1 - alpha) * background[y:y+h, x:x+w, c]    # Parte visível do fundo
                )
        else:  # Imagem sem transparência (RGB)
            background[y:y+h, x:x+w] = overlay
        
        return background
    
    # ========================================
    # MÉTODO: Listar Câmeras Disponíveis
    # ========================================
    def list_cameras(self):
        """
        Detecta todas as câmeras disponíveis no sistema.
        
        Returns:
            list: Lista com os índices das câmeras disponíveis (ex: [0, 1, 2])
        
        Nota:
            Testa até 10 possíveis câmeras (índices 0-9)
        """
        available_cameras = []
        print("\n🔍 Procurando câmeras disponíveis...")
        
        # Testar índices de 0 a 9
        for i in range(10):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                available_cameras.append(i)
                cap.release()  # Liberar a câmera
        
        return available_cameras
    
    # ========================================
    # MÉTODO: Selecionar Câmera
    # ========================================
    def select_camera(self):
        """
        Permite ao usuário escolher qual câmera usar.
        
        Returns:
            int: Índice da câmera selecionada (ou None se nenhuma disponível)
        
        Comportamento:
            - Se apenas 1 câmera: usa automaticamente
            - Se múltiplas câmeras: pede para o usuário escolher
            - Se nenhuma câmera: retorna None
        """
        cameras = self.list_cameras()
        
        # Nenhuma câmera encontrada
        if not cameras:
            print("❌ Nenhuma câmera encontrada!")
            return None
        
        print(f"\n📹 Câmeras disponíveis: {cameras}")
        
        # Apenas uma câmera - usar automaticamente
        if len(cameras) == 1:
            print(f"✅ Usando câmera {cameras[0]}")
            return cameras[0]
        
        # Múltiplas câmeras - pedir escolha do usuário
        while True:
            try:
                choice = input(f"\nEscolha a câmera {cameras} (padrão: {cameras[0]}): ").strip()
                
                # Se usuário pressionar ENTER, usar câmera padrão
                if choice == "":
                    return cameras[0]
                
                # Validar escolha
                choice_int = int(choice)
                if choice_int in cameras:
                    return choice_int
                else:
                    print(f"⚠️  Câmera {choice_int} não está disponível. Escolha entre: {cameras}")
            
            except ValueError:
                print("⚠️  Por favor, digite um número válido.")
            except KeyboardInterrupt:
                print("\n\n❌ Operação cancelada pelo usuário.")
                return None
    
    # ========================================
    # MÉTODO PRINCIPAL: Loop de Execução
    # ========================================
    def run(self, camera_id=None):
        """
        Executa o loop principal do rastreador de gestos.
        
        Args:
            camera_id: Índice da câmera a usar (None = pedir ao usuário)
        
        Fluxo de Execução:
            1. Selecionar/abrir câmera
            2. Capturar frame
            3. Detectar mãos
            4. Reconhecer gestos
            5. Exibir resultado + imagem do macaco
            6. Repetir até usuário pressionar 'q'
        """
        
        # ========================================
        # Inicialização da Câmera
        # ========================================
        if camera_id is None:
            camera_id = self.select_camera()
            if camera_id is None:
                return
        
        cap = cv2.VideoCapture(camera_id)
        
        if not cap.isOpened():
            print(f"❌ Erro: Não foi possível abrir a câmera {camera_id}")
            return
        
        # ========================================
        # Informações Iniciais
        # ========================================
        print("\n" + "=" * 60)
        print("🎥 CÂMERA INICIADA!")
        print("=" * 60)
        print(f"📹 Usando câmera: {camera_id}")
        print("\n👋 GESTOS DISPONÍVEIS:")
        print("   ☝️  Dedo indicador para cima")
        print("   😏 Dedo no canto da boca")
        print("   🫱 Mão no peito")
        print("   😐 Neutro (sem gesto específico)")
        print("\n⌨️  Pressione 'q' para sair")
        print("=" * 60 + "\n")
        
        # ========================================
        # Loop Principal
        # ========================================
        while cap.isOpened():
            # Capturar frame da câmera
            success, image = cap.read()
            
            if not success:
                print("⚠️  Frame vazio - ignorando...")
                continue
            
            # ========================================
            # Pré-processamento da Imagem
            # ========================================
            # Espelhar horizontalmente (efeito espelho mais natural)
            image = cv2.flip(image, 1)
            
            # Converter de BGR (OpenCV) para RGB (MediaPipe)
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image_rgb.flags.writeable = False  # Otimização de performance
            
            # ========================================
            # Detecção de Mãos
            # ========================================
            results = self.hands.process(image_rgb)
            
            # Converter de volta para BGR
            image_rgb.flags.writeable = True
            image = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
            
            # ========================================
            # Processar Mãos Detectadas
            # ========================================
            if results.multi_hand_landmarks and results.multi_handedness:
                # Iterar sobre cada mão detectada
                for hand_landmarks, handedness in zip(
                    results.multi_hand_landmarks, 
                    results.multi_handedness
                ):
                    # Desenhar landmarks (pontos e conexões) na imagem
                    self.mp_drawing.draw_landmarks(
                        image,
                        hand_landmarks,
                        self.mp_hands.HAND_CONNECTIONS,
                        self.mp_drawing_styles.get_default_hand_landmarks_style(),
                        self.mp_drawing_styles.get_default_hand_connections_style()
                    )
                    
                    # Detectar o gesto
                    hand_label = handedness.classification[0].label  # "Left" ou "Right"
                    gesture = self.detect_gesture(hand_landmarks.landmark, hand_label)
                    self.current_gesture = gesture
                    
                    # Exibir nome do gesto na tela
                    cv2.putText(
                        image,
                        f"Gesto: {gesture}",
                        (10, 30),                      # Posição (x, y)
                        cv2.FONT_HERSHEY_SIMPLEX,      # Fonte
                        1,                              # Tamanho
                        (0, 255, 0),                   # Cor verde (BGR)
                        2                               # Espessura
                    )
            else:
                # Nenhuma mão detectada - gesto neutro
                self.current_gesture = "neutral"
            
            # ========================================
            # Exibir Imagem do Macaco
            # ========================================
            if self.current_gesture in self.monkey_images:
                monkey_img = self.monkey_images[self.current_gesture]
                
                # Posicionar no canto superior direito
                x_offset = image.shape[1] - 320  # 20px de margem
                y_offset = 10                     # 10px do topo
                
                image = self.overlay_image(image, monkey_img, x_offset, y_offset)
            
            # ========================================
            # Exibir Frame
            # ========================================
            cv2.imshow('Rastreador de Gestos com Macaco 🐒', image)
            
            # ========================================
            # Verificar Tecla Pressionada
            # ========================================
            if cv2.waitKey(5) & 0xFF == ord('q'):
                print("\n👋 Saindo...")
                break
        
        # ========================================
        # Limpeza e Encerramento
        # ========================================
        cap.release()
        cv2.destroyAllWindows()
        print("✅ Programa encerrado com sucesso!")
        print("=" * 60 + "\n")

# ============================================================
# FUNÇÃO PRINCIPAL
# ============================================================
def main():
    """
    Ponto de entrada do programa.
    
    Função:
        - Exibe banner inicial
        - Cria instância do rastreador
        - Inicia o loop de detecção
    """
    # Banner de boas-vindas
    print("\n" + "=" * 60)
    print("🐒 RASTREADOR DE GESTOS COM MACACO 🐒")
    print("=" * 60)
    print("Sistema de reconhecimento de gestos em tempo real")
    print("Desenvolvido com OpenCV e MediaPipe")
    print("=" * 60)
    
    try:
        # Criar e executar o rastreador
        tracker = GestureTracker()
        tracker.run()
    
    except KeyboardInterrupt:
        print("\n\n❌ Programa interrompido pelo usuário (Ctrl+C)")
        print("=" * 60 + "\n")
    
    except Exception as e:
        print(f"\n\n❌ Erro inesperado: {e}")
        print("=" * 60 + "\n")
        raise


# ============================================================
# EXECUÇÃO DO PROGRAMA
# ============================================================
if __name__ == "__main__":
    main()
    main()
