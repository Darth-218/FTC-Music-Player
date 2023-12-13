import flet as ft
import vlc
import time

sound_file = r"C:\Users\alisa\Downloads\Romantic Homicide - D4vd (Slowed  reverb  Extended).mp3"
url = r"C:\Users\alisa\Downloads\Travis Scott - FE!N (Official Audio) ft. Playboi Carti.mp3"

  
def main(page: ft.Page):
    global playerState
    page.vertical_alignment= ft.MainAxisAlignment.CENTER

    def changeButtonIcon():
        if playerState == 'playing':
            setattr(play_btn, 'icon', 'pause_circle')
        else:
            setattr(play_btn, 'icon', 'play_circle')
        page.update()

    def stateChangedHandler(data):
        global playerState
        playerState = data
        print(data)
        changeButtonIcon()

    audio1 = ft.Audio(
        src=url,
        autoplay=True,
        volume=1,
        on_position_changed=lambda e: print("Position changed:", e.data),
        on_duration_changed=lambda e: print("Duration changed:", e.data),
        on_state_changed=lambda e: stateChangedHandler(e.data)
        )

    play_btn = ft.IconButton(icon='play_circle', icon_size=40, on_click=lambda e: playPauseBtnClicked())

    def playPauseBtnClicked():
        if playerState == 'playing':
            audio1.pause()
        else:
            audio1.resume()
            print('should resume')


    def volume_down(_):
        audio1.volume -= 0.1
        audio1.update()


    def volume_up(_):
        audio1.volume += 0.1
        audio1.update()


    duration = ft.Audio(on_duration_changed=lambda e: (e.data))
    
    

    
    page.overlay.append(audio1)


    previuos_btn = ft.IconButton(icon='skip_previous', icon_size=40,on_click=lambda _: audio1.seek(2000)) 

    #stop_btn = ft.IconButton(icon='stop_circle', icon_size=40, on_click=lambda _: audio1.release())

    next_btn = ft.IconButton(icon='skip_next', icon_size=40, on_click=lambda _: audio1.seek(duration))

    volume_up_btn = ft.IconButton(icon='volume_up', icon_size=34, on_click=volume_up)
    
    volume_down_btn = ft.IconButton(icon='volume_down', icon_size=40, on_click=volume_down)

    row = ft.Row(controls=[previuos_btn,play_btn,next_btn,volume_down_btn,volume_up_btn],
                 alignment=ft.MainAxisAlignment.CENTER)
    
    

    page.add(row)




ft.app(target=main)