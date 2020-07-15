from django.shortcuts import render, HttpResponse, redirect
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import shutil
import csv

# Create your views here.
def index(request):
    return redirect('login/')

def loginuser(request):
    return render(request, 'login.html')

def logoutuser(request):
    logout(request)
    return redirect('/')

def submitlogin(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        usuario = authenticate(username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect('/monitordiretorio')
        else:
            messages.error(request, "Usuário ou senha inválida.")
    return redirect('/')

@login_required(login_url='/login/')
def monitordiretorio(request):
    hora = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    dados = {'hora': hora}
    src = '/media/TWS/MonitorDeDiretorios/Csv/resultscript.csv'
    dst = '/media/TWS/MonitorDeDiretorios/Csv/resultapp.csv'
    arquivocsv = list(csv.reader(open(src, 'r')))
    arquivocsv = list(csv.reader(open(src, 'r')))
    lista_cache = []
    for line in arquivocsv:
        if line.__len__() > 0:
            lista_cache.append(line)
    count = sum(1 for line in lista_cache)
    if count > 0:
        shutil.copy(src, dst)
    arquivocsv = list(csv.reader(open(dst, 'r')))
    lista_pendente = []
    lista_arquivos = []
    for itens in arquivocsv:
        itens[3] = int(itens[3])
        itens[4] = int(itens[4])
        if itens[4] > 0:
            lista_pendente.append(itens)
        elif itens[3] > 0 and itens[4] == 0:
            lista_arquivos.append(itens)
    dados['noprazo'] = lista_arquivos
    dados['pendentes'] = lista_pendente
    return render(request, 'monitor.html', dados)

@login_required(login_url='/login/')
def monitorartodos(request):
    hora = datetime.now().strftime('%d/%m/%Y %H:%M')
    dst = '/media/TWS/MonitorDeDiretorios/Csv/resultapp.csv'
    arquivocsv = list(csv.reader(open(dst, 'r')))
    dados = {'todos': arquivocsv, 'hora': hora}
    return render(request, 'monitortodos.html', dados)

def teste():
    arquivocsv = csv.reader(open(src, 'r'))
    dados = {'dados' : arquivocsv}
    lista_pendente = []
    lista_arquivos = []
    for itens in arquivocsv:
        itens[3] = int(itens[3])
        itens[4] = int(itens[4])
        if itens[4] > 0:
            lista_pendente.append(itens)
        elif itens[3] > 0 and itens[4] == 0:
            lista_arquivos.append(itens)
    print(lista_pendente)
    print(lista_arquivos)


if __name__ == '__main__':
    teste()
