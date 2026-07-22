import re
def formatar_telefone_whatsapp(telefone_bruto, ddd_padrao="61"):
   
    if not telefone_bruto:
        return None

    numeros = re.sub(r'\D', '', telefone_bruto)
    
    if len(numeros) > 11 and numeros.startswith(ddd_padrao):
        numeros = numeros[:11]
        
    if len(numeros) == 9 and numeros.startswith('9'):
        numeros = ddd_padrao + numeros
        
    elif len(numeros) == 8:
        numeros = ddd_padrao + numeros

    if len(numeros) == 11 and numeros[2] == '9':
        ddd = numeros[:2]
        parte1 = numeros[2:7]  
        parte2 = numeros[7:]   
        
        return f"+55 {ddd} {parte1}-{parte2}"
    
    return None

arquivo_entrada = 'lista.csv'
arquivo_saida = 'contatos.vcf'

contadores = {'processados': 0, 'convertidos': 0, 'ignorados': 0}

print("Iniciando a higienização e formatação dos contatos...\n")

with open(arquivo_entrada, 'r', encoding='utf-8') as arquivo_csv, \
     open(arquivo_saida, 'w', encoding='utf-8') as arquivo_vcf:
    
    linhas = arquivo_csv.readlines()
    
    for linha in linhas:
        dados = linha.strip().split(';')
        if len(dados) < 2:
            continue
            
        contadores['processados'] += 1
        nome = dados[0].strip()
        telefone_bruto = dados[1].strip()
        
        telefone_formatado = formatar_telefone_whatsapp(telefone_bruto, ddd_padrao="61")
        
        if not telefone_formatado:
            print(f"[IGNORADO] {nome} - Incompleto, CPF ou Fixo: '{telefone_bruto}'")
            contadores['ignorados'] += 1
            continue
            
        arquivo_vcf.write("BEGIN:VCARD\n")
        arquivo_vcf.write("VERSION:3.0\n")
        arquivo_vcf.write(f"FN:{nome}\n")
        arquivo_vcf.write(f"TEL;TYPE=CELL,VOICE:{telefone_formatado}\n")
        arquivo_vcf.write("END:VCARD\n")
        
        contadores['convertidos'] += 1

print("\n-------------------------------------------")
print(f" Concluído!")
print(f" - Contatos formatados e salvos: {contadores['convertidos']}")
print(f" - Descartados (Inválidos/CPFs): {contadores['ignorados']}")
print(" Importe o novo 'contatos.vcf' no seu celular!")
print("-------------------------------------------")
