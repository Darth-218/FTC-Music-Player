import flet as ft 
import config
import ui_builder








class system_widget(ft.UserControl):

    string_Afifi = ft.Text("""\tMeet the former leader of the team while we were making the best
presentation the university has ever seen (and will ever see, unless we
decide to make another one in the future)! This guy has made his very own
music streaming mobile application in dart, not to mention countless
arduino projects in the microprocessor's modified C++; from an AC remote
controllable from your laptop to hacking the Pentagon (one of these is
true, not sure which one), this dude's got you covered.""", size=15, text_align=ft.TextAlign.LEFT)

    string_zein = ft.Text("""\tIt is never very hard to find this guy, all you have to do is look for
someone with impeccable fashion sense and a great hat. From Magic: the
Gathering to YuGiOh! to Flesh and Blood to any
variant of  he'll dominate you in any card game you
challenge him at. He's also proficient in many languages, including
Python, C#, C++, Rust, Haskell, and Uiua; not to mention human languages.""", size=15, text_align=ft.TextAlign.LEFT)

    string_yahia = ft.Text("""\tComing all the way from the most expensive city in (the Egyptian version
of) Monopoly, el-Moqattam, our team leader has absolutely no fear. Either that
or he's suicidal. I'm not sure which. What I do know, however,
is that he's made multiple projects in Python before.""", size=15, text_align=ft.TextAlign.LEFT)

    string_AbdElmaboud = ft.Text("""\tHe's completely unbeatable in League of Legends and Elden Ring, and he's
won a free ticket to Sa'yet el Sāwi by just being so damn awesome.
Fun fact: he went to the same school as our very own Ahmed Mohamed Afifi!""", size=15, text_align=ft.TextAlign.LEFT)

    def __init__(self):
        super().__init__()
        self.numberOfArtistsPerInterest = ft.TextField(width=120, border_color='grey94')

        self.numberOfAlbumsPerInterest = ft.TextField(width=120, border_color='grey94')

        self.numberOfSongsPerInterest = ft.TextField(width=120, border_color='grey94')

        self.numberOfSearchArtists = ft.TextField(width=120, border_color='grey94')

        self.numberOfSearchAlbums = ft.TextField(width=120, border_color='grey94')

        self.numberOfSearchSongs = ft.TextField(width=120, border_color='grey94')

        self.interest = ft.TextField()

    def build(self):
        return ft.Container(ft.Column(
            [
                ft.Row([
                    ft.Text("Appearance", size=20),
                    ft.Dropdown(
                        width=125,
                        border_color='grey94',
                        options=[
                            ft.dropdown.Option('Light mode'),
                            ft.dropdown.Option('Dark mode'),
                ],
                ),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),

            
            ft.Row(
                [
                    ft.Text('number Of Artists Per Interest', size=20),
                    self.numberOfArtistsPerInterest,
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),

            ft.Row(
                [
                    ft.Text('number Of Albums Per Interest', size=20),
                    self.numberOfAlbumsPerInterest,
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),

            ft.Row(
                [
                    ft.Text('number Of Songs Per Interest', size=20),
                    self.numberOfSongsPerInterest,
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),

            ft.Row(
                [
                    ft.Text('number Of Search Artists', size=20),
                    self.numberOfSearchArtists,
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),

            ft.Row(
                [
                    ft.Text('number Of Search Albums', size=20),
                    self.numberOfSearchAlbums,
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),

            ft.Row(
                [
                    ft.Text('number Of Search Songs', size=20),
                    self.numberOfSearchSongs,
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),

            ft.Row(
                [
                    ft.OutlinedButton('Save', width=120, on_click=self.on_save),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),

            ft.Row(
                [
                    ft.OutlinedButton("Add interest", on_click=self.open_dialouge),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),

            ft.Row(
                [
                    ft.OutlinedButton('About Us', on_click=self.Open_About_us_popup),
                    
                    
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),

            ft.Row(
                [
                    ft.OutlinedButton('contributors')
                ]
            )


        ],
        spacing=40,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
        width=800,
        ),
        expand=1,
        alignment=ft.alignment.center,
        )
    
    def on_save(self, e):

        if self.numberOfArtistsPerInterest.value:
            config.numberOfArtistsPerInterest = self.numberOfArtistsPerInterest.value

        if self.numberOfAlbumsPerInterest.value:
            config.numberOfAlbumsPerInterest = self.numberOfAlbumsPerInterest.value

        if self.numberOfSongsPerInterest.value:
            config.numberOfSongsPerInterest = self.numberOfSongsPerInterest.value

        if self.numberOfSearchArtists.value:
            config.numberOfSearchArtists = self.numberOfSearchArtists.value

        if self.numberOfSearchAlbums.value:
            config.numberOfSearchAlbums = self.numberOfSearchAlbums.value

        if self.numberOfSearchSongs.value:
            config.numberOfSearchSongs = self.numberOfSearchSongs.value


    def Open_About_us_popup(self, e):
        while self.page is None:
            pass

        setattr(self.page.dialog, 'modal', False)
        setattr(self.page.dialog, 'title', ft.Text('About Us'))
        setattr(self.page.dialog, 'content', ft.Column(
            [
                ft.Row(controls=[
                    ft.Image('./Assets/Images/ftc.png', width=300, height=300),
                    ft.Image('./Assets/Images/ftc.png', width=300, height=300),
                ]),
                ft.Text('Ahmed Afifi', size=30),
                    self.string_Afifi, 
                ft.Text('Zein Hatem Hafez', size=30), 
                    self.string_zein,
                ft.Text('Yahia Hany Gaber', size=30),
                    self.string_yahia,
                ft.Text('Ahmed Abdelmaboud', size=30),
                    self.string_AbdElmaboud,]))
        # setattr(self.page.dialog, 'actions', [ft.ElevatedButton('Close', on_click=self.Close_About_us_popup)])
        setattr(self.page.dialog, 'open', True)

        self.page.update()


    def Close_About_us_popup(self, e):
        while self.page is None:
            pass

        setattr(self.page.dialog, 'open', False)
        self.page.update()


    def add_interest(self, e):
        if self.interest.value:
            if config.interests2 == '':
                config.interests2 += f'{self.interest.value}--)0'
            else:
                config.interests2 += f'|*|{self.interest.value}--)0'
            while self.page is None:
                pass
            setattr(self.page.dialog, 'open', False)
            self.page.update()
            print(config.interests2)


    def close_popup(self, e):
            setattr(self.page.dialog, 'open', False)
            self.page.update()


    def open_dialouge(self, e):
        while self.page is None:
            pass

        setattr(self.page.dialog, 'modal', True)
        setattr(self.page.dialog, 'title', ft.Text('Add Interest'))
        setattr(self.page.dialog, 'content', self.interest)
        setattr(self.page.dialog, 'actions', [ft.ElevatedButton('Add', on_click=self.add_interest), ft.ElevatedButton('Close', on_click=self.close_popup)])
        setattr(self.page.dialog, 'open', True)

        self.page.update()


    