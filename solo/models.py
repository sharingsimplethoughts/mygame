from django.db import models
from registration.models import *

game_types=(('1','solo'),('2','group'),('3','multiplayer'))

# Create your models here..
class Hand(models.Model):
    title=models.CharField(max_length=20,blank=True,null=True)
    hand_image=models.ImageField(upload_to='solo/hand',blank=True,null=True)

    def __str__(self):
        return self.title

class Coin(models.Model):
    title=models.CharField(max_length=20,blank=True,null=True)
    coin_image=models.ImageField(upload_to='solo/coin',blank=True,null=True)

    def __str__(self):
        return self.title

class Game(models.Model):
    game_type=models.CharField(max_length=50, choices=game_types)
    max_number_of_players=models.PositiveIntegerField(default=2)
    max_rounds=models.PositiveIntegerField(default=3)
    max_play_time=models.PositiveIntegerField(default=30)
    max_resume_time=models.PositiveIntegerField(default=120)
    room = models.CharField(max_length=500, blank=True, null=True)
    players = models.ManyToManyField(RegisteredUser, related_name='game_players', through='GamePlayerManager')
    created_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    
    def __str__(self):
        return str(self.id)

class GamePlayerManager(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='gpm_game')
    player = models.ForeignKey(RegisteredUser,on_delete=models.CASCADE, related_name='gpm_player')
    hand = models.ForeignKey(Hand, on_delete=models.CASCADE, related_name='gpm_hand', blank=True, null=True)
    coin = models.ForeignKey(Coin, on_delete=models.CASCADE, related_name='gpm_coin', blank=True, null=True)
    total_game_point = models.PositiveIntegerField(default=0)
    is_game_winner = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return str(self.id)

class Round(models.Model):
    room = models.CharField(max_length=500, blank=True, null=True)
    round_number = models.PositiveIntegerField(default=0)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='ro_game', null=True)
    player = models.ForeignKey(RegisteredUser,on_delete=models.CASCADE, related_name='ro_player')
    prediction = models.PositiveIntegerField(default=0)
    actual = models.PositiveIntegerField(default=0)
    round_point = models.PositiveIntegerField(default=0)
    is_round_winner = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __set__(self):
        return str(self.id)

class ChatMessage(models.Model):
    room        = models.CharField(max_length=200,blank=True,null=True)
    user        = models.ForeignKey(RegisteredUser, on_delete=models.CASCADE, related_name="ch_user")
    message     = models.TextField()
    timestamp   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)












# class Player(models.Model):
#     ruser=models.ForeignKey(RegisteredUser,on_delete=models.CASCADE, related_name='pl_ruser')
#     level=models.ForeignKey(Level,on_delete=models.CASCADE,related_name='pl_level')
#     total_points=models.PositiveIntegerField(default=0)
#
#     def __str__(self):
#         return player.user.first_name + '---' + str(self.level)

# class Room(models.Model):
#     game=models.ForeignKey(Game,on_delete=models.CASCADE, related_name='r_game')
#     players = models.ManyToManyField(RegisteredUser, related_name='room_players', through='RoomManager')
#     started_by = models.ForeignKey(RegisteredUser, on_delete=models.CASCADE, related_name='r_started_by', blank=True, null=True)
#     created_on=models.DateTimeField(auto_now_add=True)
#     socket_room_id=models.CharField(max_length=300, blank=True, null=True)
#     # winner = models.ForeignKey(RegisteredUser, on_delete=models.CASCADE, related_name='r_room_winner',null=True,blank=True)

#     def __str__(self):
#         return str(self.id)+'---'+self.game.game_type

# class RoomManager(models.Model):
#     room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='rm_room')
#     player = models.ForeignKey(RegisteredUser, on_delete=models.CASCADE, related_name='rm_player')
#     is_online = models.BooleanField(default=False)
#     inactive_duration = models.PositiveIntegerField(default=0)
#     hand = models.ForeignKey(Hand, on_delete=models.CASCADE, related_name='rm_hand', blank=True, null=True)
#     coin = models.ForeignKey(Coin, on_delete=models.CASCADE, related_name='rm_coin', blank=True, null=True)
#     total_game_points=models.PositiveIntegerField(default=0)
#     is_game_winner = models.BooleanField(default=False)

#     def __str__(self):
#         return str(self.room.id)+ '---' + self.room.game.game_type + '---' + self.player.name


# class UserOnlineStatus(models.Model):
#     ruser=models.ForeignKey(RegisteredUser, on_delete=models.CASCADE, related_name='os_ruser')
#     is_online=models.PositiveIntegerField(default=0)  #0-offline, 1-online, 2-resume
#     exit_time = models.DateTimeField(default=datetime.now)
#     offline_duration = models.PositiveIntegerField(default=0)
#     is_engaged = models.BooleanField(default=False)
#     room = models.ForeignKey(Room,on_delete=models.CASCADE, related_name='os_room')
#
#     def __str__(self):
#         return self.ruser.name + '---' + self.is_online

# class GameRoom(models.Model):
#     game = models.ForeignKey(Game,on_delete=models.CASCADE,related_name='gh_game')
#     room_started_on = models.DateTimeField(auto_now_add=True)
#     player = models.ForeignKey(GamePlayer,on_delete=models.CASCADE, related_name='gh_player')
#     is_room_creator = models.BooleanField(default=False)
#     hand = models.ForeignKey(Hand,on_delete=models.CASCADE, related_name='gh_hand')
#     coin = models.ForeignKey(Coin,on_delete=models.CASCADE,related_name='gh_coin')
#     total_game_point = models.PositiveIntegerField(default=0)
#     is_game_winner = models.BooleanField(default=False)
#
#     def __str__(self):
#         return str(self.id)+'---'+self.game.game_type

# class Round(models.Model):
#     gameroom=models.ForeignKey(GameRoom,on_delete=models.CASCADE,related_name='ro_gameplay')
#     round_number=models.PositiveIntegerField(default=0)
#     player=models.ForeignKey(GamePlayer,on_delete=models.CASCADE, related_name='ro_player')
#     is_active=models.BooleanField(default=True) #to update online status
#     inactive_duration=models.PositiveIntegerField(default=0) #update for how much time is inactive
#     is_playing=models.BooleanField(default=True) #remove the player from game either by manual exit or exceding inactive duration
#     prediction=models.PositiveIntegerField(default=0)
#     actual=models.PositiveIntegerField(default=0)
#     round_point=models.PositiveIntegerField(default=0)
#     is_round_winner=models.BooleanField(default=False)
#
#     def __str__(self):
#         return str(self.gameroom.id)+'---'+str(self.gameroom.game.game_type)+'---'+str(self.round_number)


# hand_choices=(('1','H1'),('2','H2'),('3','H3'),('4','H4'))
# coin_choices=(('1','C1'),('2','C2'),('3','C3'),('4','C4'))

# class Points(models.Model):
#     ruser=models.ForeignKey(RegisteredUser,on_delete=models.CASCADE,related_name='p_ruser')
#     level=models.PositiveIntegerField(default=0)
#     total_points=models.PositiveIntegerField(default=0)
#     def __str__(self):
#         return self.ruser.name+'---'+str(self.level)+'---'+str(self.total_points)
#
# class SoloGame(models.Model):
#     player1=models.ForeignKey(RegisteredUser,on_delete=models.CASCADE,related_name='sg_player1')
#     player1_hand=models.CharField(max_length=1,choices=hand_choices)
#     player1_coin=models.CharField(max_length=1,choices=coin_choices)
#     player1_point=models.PositiveIntegerField(default=0)
#     player2=models.ForeignKey(RegisteredUser,on_delete=models.CASCADE,related_name='sg_palyer2')
#     player2_hand=models.CharField(max_length=1,choices=hand_choices)
#     player2_coin=models.CharField(max_length=1,choices=coin_choices)
#     player2_point=models.PositiveIntegerField(default=0)
#     player3=models.ForeignKey(RegisteredUser,on_delete=models.CASCADE,related_name='sg_palyer3')
#     player3_hand=models.CharField(max_length=1,choices=hand_choices)
#     player3_coin=models.CharField(max_length=1,choices=coin_choices)
#     player3_point=models.PositiveIntegerField(default=0)
#
#     winner=models.ForeignKey(RegisteredUser,on_delete=models.CASCADE,related_name='sg_winner')
#
#     def __str__(self):
#         return str(self.id)+'---'+str(self.winner.name)
#
# class SoloGameRound(models.Model):
#     game=models.ForeignKey(SoloGame,on_delete=models.CASCADE,name='game')
#     round_number=models.PositiveIntegerField(default=0)
#     player1=models.ForeignKey(RegisteredUser,on_delete=models.CASCADE,related_name='sgr_player1')
#     player1_point=models.PositiveIntegerField(default=0)
#     player2=models.ForeignKey(RegisteredUser,on_delete=models.CASCADE,related_name='sgr_palyer2')
#     player2_point=models.PositiveIntegerField(default=0)
#     player3=models.ForeignKey(RegisteredUser,on_delete=models.CASCADE,related_name='sgr_palyer3')
#     player3_point=models.PositiveIntegerField(default=0)
#
#     winner=models.ForeignKey(RegisteredUser,on_delete=models.CASCADE,related_name='sgr_winner')
#
#     def __str__(self):
#         return str(self.id)+'---'+str(self.winner.name)
