# ライブラリのインポート
import requests
import tarfile
import os
import shutil
from PIL import Image
import wget
import sys
from tqdm import tqdm
import time

# URLからtgzファイルをダウンロードする関数
def download_tgz(url, filename):
    # ダウンロードする
    wget.download(url)
    print('\nDownload completed.')

# tgzファイルを展開する関数
def extract_tgz(filename):
    with tarfile.open(filename, 'r:gz') as tar:
        tar.extractall()
    # tgzファイルを閉じる
    tar.close()
    print('Extraction to folder.')
    print('Extraction completed.')

# 画像ファイルをリサイズする関数
def resize_images(folder,size):
    print('Resizing images.')
    print('パス：',folder)
    # フォルダ"pose"と”mask”削除
    try:
        shutil.rmtree(folder+'/poses')
        shutil.rmtree(folder+'/masks')
    except OSError:
        print('Could not remove the folder... Pass...')
        pass
    os.remove(folder+'/calibration.h5')
    
    files = os.listdir(folder)
    files_file = [f for f in files if os.path.isfile(os.path.join(folder, f))]
    
    # フォルダ内の画像ファイルに対して繰り返す
    for file in tqdm(files_file):
        # 画像ファイルを開く
        img = Image.open(folder + '/' + file)
        # リサイズする
        img_resize = img.resize(size)
        # ファイル名を変更する
        img_resize.save(folder + '/' + file)
    
    print('Resizing completed.')

def rename_image_file(folder):
    files = os.listdir(folder)
    files_file = [f for f in files if os.path.isfile(os.path.join(folder, f))]
    time_file = int(time.time())
    num = 0
    for file in files_file:
        os.rename(folder + '/' + file, folder + '/' + str(time_file) + str(num)+'.jpg')
        num += 1
    # 1sec wait
    time.sleep(1)

# URLのベースを指定する
base_url = 'http://ycb-benchmarks.s3-website-us-east-1.amazonaws.com/'
# オブジェクトの番号のリストを作成する
object_numbers = ['001','002','003','004','005','006','007','008','009','010','011','012','013','014','015','016','017','018','019','021','022','024','025'
                  ,'026','027','029','030','031','032','033','035','036','037','038','039','040','041','042','043','044','048','049','050','051','052','053'
                  ,'054','055','056','057','058','059','061','062','063-a','063-b','063-c','063-d','063-e','063-f','065-a','065-b','065-c','065-d','065-e',
                  '065-f','065-g','065-h','065-i','065-j','070-a','071','072-a','072-b','072-c','072-d','072-e','072-f','072-g','072-h','072-i','072-j',
                  '072-k','073-a','073-b','073-c','073-d','073-e','073-f','073-g','073-h','073-i','073-j','073-k','073-l','073-m','076','077'
]
# オブジェクトの名前のリストを作成する
object_names = [
            'chips_can', 'master_chef_can', 'cracker_box', 
            'sugar_box', 'tomato_soup_can', 'mustard_bottle', 
            'tuna_fish_can', 'pudding_box', 'gelatin_box', 
            'potted_meat_can', 'banana','strawberry',
            'apple','lemon','peach','pear','orange','plum',
            'pitcher_base','bleach_cleanser','windex_bottle','bowl','mug',
            'sponge','skillet','plate','fork','spoon',
            'knife','spatula','power_drill','wood_block',
            'scissors','padlock','key','large_marker',
            'small_marker','adjustable_wrench','phillips_screwdriver',
            'flat_screwdriver','hammer','small_clamp','medium_clamp',
            'large_clamp','extra_large_clamp','mini_soccer_ball',
            'softball','baseball','tennis_ball','racquetball',
            'golf_ball','chain','foam_brick','dice',
            'marbles_a','marbles_b','marbles_c','marbles_d','marbles_e','marbles_f',
            'cups_a','cups_b','cups_c','cups_d','cups_e','cups_f','cups_g','cups_h','cups_i','cups_j',
            'colored_wood_blocks_a',
            'nine_hole_peg_test','toy_airplane_a','toy_airplane_b','toy_airplane_c','toy_airplane_d',
            'toy_airplane_e','toy_airplane_f','toy_airplane_g','toy_airplane_h','toy_airplane_i','toy_airplane_j',
            'toy_airplane_k','lego_duplo_a','lego_duplo_b','lego_duplo_c','lego_duplo_d','lego_duplo_e','lego_duplo_f',
            'lego_duplo_g','lego_duplo_h','lego_duplo_i','lego_duplo_j','lego_duplo_k','lego_duplo_l','lego_duplo_m',
            'timer','rubiks_cube'
]

cwd = os.getcwd()
print("Current working directory is:", cwd)

# オブジェクトの番号と名前に対して繰り返す
for number, name in  zip(object_numbers, object_names):
    if not os.path.exists(cwd + '/' + name):
        
        # 新しいフォルダを作成する
        new_folder = '{}'.format(name)
        if (number == '063-a'or number == '063-b'or number =='063-c'
            or number =='063-d'or number == '063-e'or number== '063-f'):
            name_a = "marbles"
            url = base_url +'data/berkeley/'+ number + '_' + name_a +'/'+ number + '_' + name_a + '_berkeley_rgb_highres.tgz'
            filename = number + '_' + name_a + '_berkeley_rgb_highres.tgz'
        elif (number == '065-a' or number == '065-b' or number == '065-c' or
            number == '065-d' or number == '065-e' or number == '065-f' or
            number == '065-g' or number == '065-h' or number == '065-i' or 
            number == '065-j'):
            name_a = "cups"
            url = base_url +'data/berkeley/'+ number + '_' + name_a +'/'+ number + '_' + name_a + '_berkeley_rgb_highres.tgz'
            filename = number + '_' + name_a + '_berkeley_rgb_highres.tgz'
        elif number == '070-a' or number == '070-b':
            name_a = "colored_wood_blocks"
            url = base_url +'data/berkeley/'+ number + '_' + name_a +'/'+ number + '_' + name_a + '_berkeley_rgb_highres.tgz'
            filename = number + '_' + name_a + '_berkeley_rgb_highres.tgz'
        elif (number == '072-a' or number == '072-b' or number == '072-c' or
            number == '072-d' or number == '072-e' or number == '072-f' or
            number == '072-g' or number == '072-h' or number == '072-i' or
            number == '072-j' or number == '072-k'):
            name_a = "toy_airplane"
            url = base_url +'data/berkeley/'+ number + '_' + name_a +'/'+ number + '_' + name_a + '_berkeley_rgb_highres.tgz'
            filename = number + '_' + name_a + '_berkeley_rgb_highres.tgz'
        elif (number == '073-a' or number == '073-b' or number == '073-c' or
                number == '073-d' or number == '073-e' or number == '073-f' or 
                number == '073-g' or number == '073-h' or number == '073-i' or
                number == '073-j' or number == '073-k' or number == '073-l' or
                number == '073-m'):
            name_a = "lego_duplo"
            url = base_url +'data/berkeley/'+ number + '_' + name_a +'/'+ number + '_' + name_a + '_berkeley_rgb_highres.tgz'
            filename = number + '_' + name_a + '_berkeley_rgb_highres.tgz'
        else:
            #! 参考：http://ycb-benchmarks.s3-website-us-east-1.amazonaws.com/data/berkeley/001_chips_can/001_chips_can_berkeley_rgb_highres.tgz
            # URLからtgzファイル名を作成する
            url = base_url +'data/berkeley/'+ number + '_' + name +'/'+ number + '_' + name + '_berkeley_rgb_highres.tgz'
            print(url)
            filename = number + '_' + name + '_berkeley_rgb_highres.tgz'
        if not os.path.exists(cwd +'/'+filename):
            print("Downloaded file({}) downloading.....".format(filename))
            # tgzファイルをダウンロードする
            download_tgz(url, filename)
            # tgzファイルを展開する
            folder_2 ="/"
        else:
            print("Downloaded file({}) already exists.".format(filename))
        extract_tgz(filename)
        
        try:    
            # FileNotFoundError: [Errno 2] No such file or directory: '063-c_marbles' -> 'marbles_c
            # 展開されたfile 名　何故か違う嫌がらせ。。。（泣）
            if number == "063-c":
                os.rename("063-3_marbles",new_folder)
            # NameError: name 'name_a' is not defined. Did you mean: 'name'? 
            # 071 展開したファイル名が違うため、変更
            elif number == "071":
                os.rename("071-1_nine_hole_peg_test",new_folder)
            else:
                os.rename(number + '_' + name , new_folder)
        
        except OSError:
            try:
                print("Could not rename the folder({})".format(name))
                # 作業ディレクトリに移動する
                shutil.copytree(cwd+'/home/bcalli/Desktop/'+number + '_' + name,cwd)
                #ホームディレクトリに削除
                shutil.rmtree(cwd+'/home')
                print('Rename again....')
                os.rename(number + '_' + name , new_folder)
            except OSError:
                print("Could not rename the folder({})".format(name))
                print('Retrying...')
                os.rename(number + '_' + name_a , new_folder)
        finally:
            print('Something is wrong....') 
            

        # 画像ファイルをリサイズする
        resize_images(new_folder, (534, 356))
        # 一時的なフォルダとダウンロードしたファイルを削除する
        os.remove(filename)
    else:
        print("The folder({}) already exists. Go to Next Object".format(name))
        
print("finished downloading into the folder")
print("start renaming... file...")
object_name_count = len(object_names) + 1
count_n =0
for data in tqdm(object_names,desc="ファイル名前変更中...",):
    rename_image_file(data)
    
print('Rename completed.')