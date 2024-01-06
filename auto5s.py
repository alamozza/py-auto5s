import shutil
import datetime
import pathlib
import os
from PIL import Image
import ffmpeg

def main():
    """
    srcpath上の画像・動画ファイルを日時情報を利用して、日時名のディレクトリを作成して
    ファイルを移動する
    """
    srcpath: str = r"/home/frasgo/tmp"
    tgtpath: str = r"/home/frasgo/tmp/tgtdir"
    todaydate: str = str(datetime.datetime.now()).replace(" ", "").replace("-", "")[:8]
    dateinfo: str = ""
    for file in [x for x in pathlib.Path(srcpath).iterdir() if x.is_file()]:
        tgtdir: pathlib.PosixPath = pathlib.Path("")
        dateinfo: str = ""
        sufx: str = file.suffix.lower()
        if any([sufx in [".jpg", ".jpeg"]]):
            # 画像データはexif情報から日時情報を取得する
            dateinfo = get_date_from_exif(file)
        elif any([sufx in [".mp4"]]):
            # 動画はffmpegから日所情報を取得する
            dateinfo = get_date_from_ffmpeg(file)
        # 
        if dateinfo == "":
            dateinfo = get_date_from_file(file)
        tgtdirops: list[pathlib.PosixPath] = [x for x in pathlib.Path(tgtpath).iterdir() \
                if x.is_dir() and str(x.name).startswith(dateinfo)]
        if len(tgtdirops) == 1:
            # すでに日時ディレクトリが1個存在する場合、そのディレクトリ上にファイルを移動する
            tgtdir = tgtdirops[0]
        elif len(tgtdirops) >= 2:
            # すでに日時ディレクトリが2個以上存在する場合、新規にディレクトリを作成する
            newdirname: str = f"{dateinfo}_on{todaydate}"
            tgtdir = pathlib.Path(tgtpath).joinpath(newdirname)
            tgtdir.mkdir(parents=True)
        else:
            # 日時ディレクトリが全く存在しない場合
            tgtdir = pathlib.Path(tgtpath).joinpath(dateinfo)
            tgtdir.mkdir(parents=True)
        newfile: pathlib.PosixPath = pathlib.Path(tgtdir).joinpath(file.name)
        if newfile.exists():
            # 移動先に同じ名前のファイルがあるときはファイル名を変更して移動する
            newfilename: str = f"{file.stem}_movedOn{todaydate}{sufx}"
            newfile = pathlib.Path(tgtdir).joinpath(newfilename)
        shutil.move(file, newfile)
    print("completed.")

def get_date_from_exif(filepath: pathlib.PosixPath) -> str:
    oneimg = Image.open(filepath)
    exif_dict = oneimg._getexif()
    oneimg.close()
    # 
    key: int = 0
    for i in [36867, 36868, 306]:
        # 36867: DateTimeOriginal
        # 36878: DateTimeDigitized
        # 306:  DateTime
        if i in exif_dict.keys():
            key = i
            break
    if key == 0:
        # raise "Key Not Found in Exif info"
        # 日時情報がexif情報から取得できない場合はファイル属性から取得する
        return ""
    dateinfo: str = exif_dict[key].replace(" ", "").replace(":", "")[:8]
    return dateinfo

def get_date_from_ffmpeg(filepath: pathlib.PosixPath) -> str:
    info: dict[str, object] = ffmpeg.probe(filepath)
    dateinfo: str = info["format"]["tags"]["creation_time"].replace("-", "")[:8]
    return dateinfo

def get_date_from_file(filepath: pathlib.PosixPath) -> str:
    # ファイルの最終更新日時を取得する getmtime
    dateinfo_float: float = os.path.getmtime(filepath)
    dateinfo: str = datetime.datetime.fromtimestamp(dateinfo_float) \
        .strftime("%Y%m%d")
    return dateinfo

if __name__ == "__main__":
    main()
