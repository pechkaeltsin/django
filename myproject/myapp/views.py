from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import UploadFileForm
import pandas as pd


def home(request):
    mismatched_rows = []

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            input_file = request.FILES['file']
            ksr_file = 'myapp/ksr.csv'
            input_data = pd.read_csv(input_file, sep='|', header=None)
            ksr_data = pd.read_csv(ksr_file, sep='|', header=None)

            match_count = sum(input_data[1] == ksr_data[0])
            total_count = len(input_data)
            match_percent = (match_count / total_count) * 100

            for index, row in input_data.iterrows():
                input_val = row[1]
                ksr_val = ksr_data.iloc[index, 0]
                if input_val != ksr_val:
                    mismatched_rows.append({'index': index+1, 'input_val': input_val, 'ksr_val': ksr_val})

            return render(request, 'myapp/home.html', {'form': form, 'match_percent': match_percent,
                                                       'mismatched_rows': mismatched_rows})
    else:
        form = UploadFileForm()
        return render(request, 'myapp/home.html', {'form': form})
