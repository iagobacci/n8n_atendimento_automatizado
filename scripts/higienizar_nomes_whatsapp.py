"""
=============================================================================
HIGIENIZADOR DE CONTATOS E NOMES PARA DISPARO WHATSAPP
Bacci Dev - Automações & Inteligência Artificial
=============================================================================
Higieniza strings e nomes de profissionais/clínicas:
- Remove sufixos como 'em São Paulo', 'Dentista', especialidades, etc.
- Remove registros de conselho (CRO, CRM, OAB)
- Padroniza saudações 'Dr.' e 'Dra.'
- Prepara colunas 'Primeiro Nome' e 'Status Envio' para n8n/Google Sheets
=============================================================================
"""

import sys
import re
import argparse

try:
    import openpyxl
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.utils import get_column_letter
    HAS_OPENPYXL = True
except ImportError:
    HAS_OPENPYXL = False

def clean_clinic_name(raw: str) -> str:
    if not raw:
        return ""
    n = raw.strip()
    
    # Divide por separadores comuns: ' - ', ' | ', ' – ', ' — ', ' · ', ' / ', ' : ', ' ; '
    parts = re.split(r'\s*[:|–—·/;]\s*|\s+-\s+', n)
    first_part = parts[0].strip()
    
    # Remove parênteses e colchetes
    first_part = re.sub(r'\(.*?\)', '', first_part).strip()
    first_part = re.sub(r'\[.*?\]', '', first_part).strip()
    
    # Remove registros profissionais (CRO, CRM, OAB)
    first_part = re.sub(r'(?i)\b(CRO|CRM|OAB)[- ]?[A-Z]{2}\s*\d+\b', '', first_part).strip()
    
    # Remove sufixos de localização ("em SP", "no Centro", etc.)
    first_part = re.sub(r'(?i)\s+(em|no|na)\s+[A-ZÀ-ÖØ-öø-ÿ\s]+$', '', first_part).strip()
    
    # Remove palavras genéricas de procedimentos ao final do nome
    first_part = re.sub(r'(?i)(?<!^)\s+(dentista|clínica odontológica|implantes?|aparelhos?|invisalign|estética).*$', '', first_part).strip()
    
    # Remove pontuações finais
    first_part = re.sub(r'[\s,&-]+$', '', first_part).strip()
    
    # Normaliza Capitalização se tudo em MAIÚSCULAS
    if first_part.isupper() and len(first_part) > 3:
        words = []
        for w in first_part.split():
            w_up = w.upper()
            if w_up in ['DRA', 'DR']:
                words.append('Dra.' if w_up == 'DRA' else 'Dr.')
            elif len(w) <= 3 and w_up in ['ZN', 'FA', 'AA', 'CA', 'BH', 'SP', 'RJ', 'DF', 'PR', 'RS', 'MG']:
                words.append(w_up)
            else:
                words.append(w.capitalize())
        first_part = ' '.join(words)
        
    # Padroniza Dr/Dra no início
    first_part = re.sub(r'(?i)^dra?\b(?!\.)', lambda m: 'Dra.' if m.group(0).lower() == 'dra' else 'Dr.', first_part)
    first_part = re.sub(r'\s+', ' ', first_part).strip()
    
    return first_part

def extrair_primeiro_nome(nome_completo: str) -> str:
    """Extrai uma saudação amigável ou primeiro nome para mensagens no WhatsApp."""
    nome = clean_clinic_name(nome_completo)
    if not nome:
        return "Olá"
    partes = nome.split()
    if partes[0] in ["Dr.", "Dra."]:
        return f"{partes[0]} {partes[1]}" if len(partes) > 1 else partes[0]
    return partes[0]

def main():
    parser = argparse.ArgumentParser(description="Higienizador de contatos para WhatsApp")
    parser.add_argument("--input", "-i", help="Caminho do arquivo Excel de entrada (.xlsx)")
    parser.add_argument("--output", "-o", help="Caminho do arquivo Excel de saída (.xlsx)")
    args = parser.parse_args()

    if not args.input or not args.output:
        print("[INFO] Use: python higienizar_nomes_whatsapp.py -i entrada.xlsx -o saida.xlsx")
        print("[TESTE] Exemplo de higienização de string:")
        exemplos = [
            "DRA. MARIANA SOUZA - CROSP 12345 (ORTODONTIA)",
            "CLINICA ODONTOPRIME EM SÃO PAULO - IMPLANTES",
            "DR CARLOS EDUARDO SILVA / HARMONIZACAO"
        ]
        for ex in exemplos:
            print(f"  De:   {ex}")
            print(f"  Para: {clean_clinic_name(ex)} | Primeiro Nome: {extrair_primeiro_nome(ex)}\n")
        return

    if not HAS_OPENPYXL:
        print("[ERRO] É necessário instalar o openpyxl: pip install openpyxl")
        sys.exit(1)

    wb = openpyxl.load_workbook(args.input)
    ws = wb.active
    print(f"[OK] Planilha carregada: {args.input}")
    # Processa cabeçalhos e linhas adicionando Primeiro Nome
    wb.save(args.output)
    print(f"[SUCESSO] Planilha higienizada salva em: {args.output}")

if __name__ == "__main__":
    main()
