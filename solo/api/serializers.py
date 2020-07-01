from rest_framework import serializers
from django.db.models import Max
from rest_framework.exceptions import APIException
from solo.models import *
from registration.models import *

class HandListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hand
        fields = '__all__'

class CoinListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coin
        fields = '__all__'

class SubmitSoloGameRoundSerializer(serializers.ModelSerializer):
    room=serializers.CharField(allow_blank=True)
    prediction=serializers.CharField(allow_blank=True)
    actual=serializers.CharField(allow_blank=True)
    round_point=serializers.CharField(allow_blank=True)
    is_round_winner=serializers.CharField(allow_blank=True)

    class Meta:
            model=Round
            fields=('room','prediction','actual','round_point','is_round_winner',)#'round_number',

    def validate(self,data):
        room=data['room']
        # round_number=data['round_number']
        prediction=data['prediction']
        actual=data['actual']
        round_point=data['round_point']
        is_round_winner=data['is_round_winner']

        if not room or room=='':
            raise APIException({
                'message':'Please provide room id',
                'success':'False',
            })
        # if not round_number or round_number=='':
        #     raise APIException({
        #         'message':'Please provide round number',
        #         'success':'False',
        #     })
        if not prediction or prediction=='':
            raise APIException({
                'message':'Please provide predicted value',
                'success':'False',
            })
        if not actual or actual=='':
            raise APIException({
                'message':'Please provide actual value',
                'success':'False',
            })
        if not round_point or round_point=='':
            raise APIException({
                'message':'Please provide points earned',
                'success':'False',
            })
        if not is_round_winner or is_round_winner=='':
            raise APIException({
                'message':'Please tell, the player is a winner or not',
                'success':'False'
            })
        if room:
            room_obj=Room.objects.filter(id=room).first()
            if not room_obj:
                raise APIException({
                    'message':'This room id is not valid',
                    'success':'False'
                })
            # game=room_obj.game
            # if round_number<1 or round_number>game.max_rounds:
            #     raise APIException({
            #         'message':'round number should be between 1 and '+str(game.max_rounds),
            #         'success':'False',
            #     })

            #this validation will be done from front end
            # count_players=Round.objects.filter(room=room_obj,round_number=round_number,is_playing='True').count()
            # if prediction<0 or prediction>(count_players*3):
            #     raise APIException({
            #         'message':'Predicted value is incorrect',
            #         'success':'False',
            #     })
            # if actual<0 or actual>(count_players*3):
            #     raise APIException({
            #         'message':'Actual value is incorrect',
            #         'success':'False',
            #     })


            if is_round_winner not in ('0','1'):
                raise APIException({
                    'message':'is round winner value is incorrect',
                    'success':'False',
                })
        return data

    def create(self,validated_data):
        room=validated_data['room']
        # round_number=validated_data['round_number']
        prediction=validated_data['prediction']
        actual=validated_data['actual']
        round_point=validated_data['round_point']
        is_round_winner=validated_data['is_round_winner']

        user=self.context['request'].user
        if user:
            ruser=RegisteredUser.objects.filter(user=user).first()
            if ruser:
                room_obj=Room.objects.filter(id=room).first()
                round = Round(
                    room = room_obj,
                    player = ruser,
                    prediction = prediction,
                    actual = actual,
                    round_point = round_point,
                    is_round_winner = True if is_round_winner else False,
                )
                round.save()

                room_manager=RoomManager.objects.filter(room=room_obj,player=ruser).first()
                room_manager.total_game_points=room_manager.total_game_points+int(round_point)
                room_manager.save()

                ruser.total_points = ruser.total_points+int(round_point)
                ruser.save()

                if ruser.total_points>ruser.level.max_points:
                    level = Level.objects.filter(level=ruser.level.level+1).first()
                    if level:
                        ruser.level = level
                        ruser.is_all_level_completed=False
                    else:
                        ruser.is_all_level_completed=True
                    ruser.save()

                # total_round=Round.objects.filter(player=ruser,room=room_obj).count()
                # if room_obj.game.max_rounds==total_round:
                max_game_point=RoomManager.objects.filter(room=room_obj).aggregate(Max('total_game_points'))
                room_users = RoomManager.objects.filter(room=room_obj)
                for i in room_users:
                    print('***************************************')
                    print(i.total_game_points)
                    print(max_game_point)
                    print('-------------------------------------')
                    if i.total_game_points==max_game_point['total_game_points__max']:
                        print(i)
                        print('88888888888888888888888888888888888')
                        i.is_game_winner=True
                    else:
                        print(i)
                        print('9999999999999999999999999999999999')
                        i.is_game_winner=False
                    i.save()
                # if room_manager.total_game_points==max_game_point:
                #     room_manager.is_game_winner = True
                # else:
                #     room_manager.is_game_winner = False
                # room_manager.save()

                # player_obj=GamePlayer.objects.filter(player=ruser).first()
                # groom_obj=Room.objects.filter(id=room,player=player_obj).first()
                # round_obj=Round.objects.filter(room=groom_obj,player=player_obj,round_number=round_number).first()
                # round_obj.prediction=prediction
                # round_obj.actual=actual
                # round_obj.round_point=round_point
                # round_obj.is_round_winner='True' if is_round_winner else 'False'
                # round_obj.save()
                # groom_obj.total_game_point=groom_obj.total_game_point+round_point
                # #update game winner
                # max_game_point=Room.objects.filter(id=room).aggregate(Max(total_game_point))
                # if groom_obj.total_game_point>=max_game_point:
                #     groom_obj.is_game_winner='True'
                # else:
                #     groom_obj.is_game_winner='False'
                # groom_obj.save()
                #
                # player_obj.total_points=player_obj.total_points+round_point
                # #check whether level up or not and update level
                # if player_obj.total_points>player_obj.level.max_points:
                #     up_level==Level.objects.filter(level=player_obj.level.level+1).first()
                #     if up_level:
                #         player_obj.level=up_level
                # player_obj.save()
                #
                # #create next round
                # next_round=Round(
                #     room=room,
                #     round_number=round_number+1,
                #     player=player_obj,
                # )
                # next_round.save()
            else:
                raise APIException({
                    'message':'No registered user found for this user',
                    'success':'False'
                })
        else:
            raise APIException({
                'message':'No user found for this token',
                'message':'False',
            })
        return validated_data

class GameStartSerializer(serializers.ModelSerializer):
    game_id = serializers.CharField(read_only=True)
    game_type=serializers.CharField(allow_blank=True)
    room=serializers.CharField(allow_blank=True)
    class Meta:
            model=Round
            fields=('game_id','game_type','room')
    def validate(self,data):
        game_type = data['game_type']
        room = data['room']
        if not game_type or game_type=='':
            raise APIException({
                'message':'Please provide game type',
                'success':'False',
            })
        if not room or room=='':
            raise APIException({
                'message':'Please provide room',
                'success':'False',
            })
        if game_type not in ['1','2','3']:
            raise APIException({
                'message':'Please provide valid game type',
                'success':'False',
            })
        
        return data
    def create(self,validated_data):
        game_type = validated_data['game_type']
        room = validated_data['room']
        ruser = self.context['ruser']
        g = Game.objects.filter(room=room,game_type=game_type).order_by('-created_on').first()
        
        if g:
            '''
            this code is done to remove the duplicacy of room 
            as well as 
            the game will not be counted which was shut down without playing a single round
            '''
            tempr = Round.objects.filter(game=g).first()
            if tempr:
                g = Game(
                    game_type = game_type,
                    room = room
                )
                g.save()
            gpm = GamePlayerManager.objects.filter(game=g,player=ruser).first()
            if gpm:
                raise APIException({
                'message':'This user already joined this game',
                'success':'False',
            })
        else:
            g = Game(
                game_type = game_type,
                room = room
            )
            g.save()

        gpm = GamePlayerManager(
            game = g,
            player = ruser,
        )
        gpm.save()
        validated_data['game_id'] = g.id
        return validated_data
        
class GameEndSerializer(serializers.ModelSerializer):
    game_id = serializers.CharField(allow_blank=True)
    room=serializers.CharField(allow_blank=True)
    round_number=serializers.CharField(allow_blank=True)
    prediction=serializers.CharField(allow_blank=True)
    actual = serializers.CharField(allow_blank=True)
    round_point=serializers.CharField(allow_blank=True)
    is_round_winner=serializers.CharField(allow_blank=True)
    is_game_winner=serializers.CharField(allow_blank=True)
    class Meta:
            model=Round
            fields=('game_id','room','round_number','prediction','actual',
            'round_point','is_round_winner','is_game_winner')
    def validate(self,data):
        game_id = data['game_id']
        room = data['room']
        round_number = data['round_number']
        prediction=data['prediction']
        actual=data['actual']
        round_point=data['round_point']
        is_round_winner=data['is_round_winner']
        is_game_winner=data['is_game_winner']
        if not game_id or game_id=='':
            raise APIException({
                'message':'Please provide game id',
                'success':'False',
            })
        if not room or room=='':
            raise APIException({
                'message':'Please provide room',
                'success':'False',
            })
        if not round_number or round_number=='':
            raise APIException({
                'message':'Please provide round_number',
                'success':'False',
            })
        if not prediction or prediction=='':
            raise APIException({
                'message':'Please provide predicted value',
                'success':'False',
            })
        if not actual or actual=='':
            raise APIException({
                'message':'Please provide actual value',
                'success':'False',
            })
        if not round_point or round_point=='':
            raise APIException({
                'message':'Please provide points earned',
                'success':'False',
            })
        if not is_round_winner or is_round_winner=='':
            raise APIException({
                'message':'Please tell, the player is a winner or not',
                'success':'False'
            })
        if not is_game_winner or is_game_winner=='':
            raise APIException({
                'message':'Please tell, the player is a winner or not',
                'success':'False'
            })
        g=''
        if game_id:
            g=Game.objects.filter(id=game_id).first()
            if not g:
                raise APIException({
                    'message':'This game id is not valid',
                    'success':'False'
                })
            
        if is_round_winner not in ('0','1'):
            raise APIException({
                'message':'is round winner value is incorrect',
                'success':'False',
            })
        if is_game_winner not in ('0','1'):
            raise APIException({
                'message':'is game winner value is incorrect',
                'success':'False',
            })
        if g:
            gpmw = GamePlayerManager.objects.filter(game=g,is_game_winner=True)
            if gpmw:
                raise APIException({
                    'message':'This game already has an winner',
                    'success':'False',
                })
        
        
        return data

    def create(self,validated_data):
        game_id = validated_data['game_id']
        room = validated_data['room']
        round_number = validated_data['round_number']
        prediction=validated_data['prediction']
        actual=validated_data['actual']
        round_point=validated_data['round_point']
        is_round_winner=validated_data['is_round_winner']
        is_game_winner=validated_data['is_game_winner']
        ruser = self.context['ruser']

        g = Game.objects.filter(id=game_id).first()

        er = Round.objects.filter(game=g,round_number=round_number,player=ruser).first()
        if er:
            raise APIException({
                'message':'Data for this round, for this game, for this user is already submitted',
                'success':'False',
            })


        round = Round(
            game = g,
            room = room,
            round_number = round_number,
            player = ruser,
            prediction = prediction,
            actual = actual,
            round_point = round_point,
            is_round_winner = True if is_round_winner else False,
        )
        round.save()
        gpm = GamePlayerManager.objects.filter(game=g,player=ruser).first()
        if int(is_game_winner) == 1:
            gpm.is_game_winner = True
        gpm.total_game_point = int(gpm.total_game_point)+int(round_point)
        gpm.save()
        ruser.total_points = int(ruser.total_points)+int(round_point)
        ruser.save()

        # update level and check is_all_level_completed
        if ruser.total_points>ruser.level.max_points:
            level = Level.objects.filter(level=ruser.level.level+1).first()
            if level:
                ruser.level = level
                ruser.is_all_level_completed=False
            else:
                ruser.is_all_level_completed=True
            ruser.save()

        return validated_data




# class CreateRoomSerializer(serializers.ModelSerializer):
#     game=serializers.CharField(allow_blank=True,allow_null=True)
#     players=serializers.CharField(allow_blank=True,allow_null=True)
#     created_on=serializers.CharField(read_only=True)
#     class Meta:
#         model=Room
#         fields=('game','players','created_on')

#     def validate(self,data):
#         game=data['game']
#         players=data['players']
#         if not game or game=="":
#             raise APIException({
#                 'message':'game id is required',
#                 'success':'False'
#             })
#         if not players or players=="":
#             raise APIException({
#                 'message':'players not provided',
#                 'success':'False',
#             })
#         if game:
#             obj=Game.objects.filter(id=game).first()
#             if not obj:
#                 raise APIException({
#                     'message':'Game id is invalid',
#                     'success':'False',
#                 })
#         if players:
#             mylist=players.split(',')
#             print(mylist)
#             print(len(mylist))
#             if len(mylist)==0:
#                 raise APIException({
#                     'message':'Please provide player ids',
#                     'success':'False',
#                 })
#             for p in mylist:
#                 ruser=RegisteredUser.objects.filter(id=p).first()
#                 if not ruser:
#                     raise APIException({
#                         'message':'Please check the player id '+str(p),
#                         'success':'False',
#                     })
            
#         return data

#     def create(self,validated_data):
#         game=validated_data['game']
#         players=validated_data['players']
#         players_list=[]
#         players_list=players.split(',')
#         obj=Game.objects.filter(id=game).first()
#         if obj:
#             room=Room(
#                 game=obj,
#             )
#             room.save()

#         for p in players_list:
#             ruser=RegisteredUser.objects.filter(id=p).first()
#             if ruser:
#                 rm=RoomManager(
#                     room=room,
#                     player=ruser,
#                 )
#                 rm.save()
#         return validated_data


# class GameStartSerializer(serializers.ModelSerializer):
#     game=serializers.CharField(allow_blank=True,)
#     hand=serializers.CharField(allow_blank=True,)
#     coin=serializers.CharField(allow_blank=True,)

#     gameroom=serializers.CharField(read_only=True)
#     is_active=serializers.CharField(read_only=True)
#     inactive_duration=serializers.CharField(read_only=True)
#     is_playing=serializers.CharField(read_only=True)

#     class Meta:
#         model=Room
#         fields=('game','hand','coin')

#     def validate(self,data):
#         game=data['game']
#         hand=data['hand']
#         coin=data['coin']

#         if not game or game=='':
#             raise APIException({
#                 'message':'Please provide game type',
#                 'success':'False',
#             })
#         if not hand or hand=='':
#             raise APIException({
#                 'message':'Please provide hand type',
#                 'success':'False',
#             })
#         if not coin or coin=='':
#             raise APIException({
#                 'message':'Please provide coin type',
#                 'success':'False',
#             })
#         game_obj=Game.objects.filter(id=game).first()
#         hand_obj=Hand.objects.filter(id=hand).first()
#         coin_obj=Coin.objects.filter(id=coin).first()

#         if not game_obj:
#             raise APIException({
#                 'message':'This game type does not exists',
#                 'success':'False',
#             })
#         if not hand_obj:
#             raise APIException({
#                 'message':'This hand type does not exists',
#                 'success':'False',
#             })
#         if not coin_obj:
#             raise APIException({
#                 'message':'This coin type does not exists',
#                 'success':'False',
#             })

#         return data

#     def create(self,validated_data):
#         game=validated_data['game']
#         hand=validated_data['hand']
#         coin=validated_data['coin']

#         user=self.context['request'].user
#         ruser=RegisteredUser.objects.filter(user=user).first()
#         player_obj=GamePlayer.objects.filter(player=ruser).first()
#         game_obj=Game.objects.filter(id=game).first()
#         hand_obj=Hand.objects.filter(id=hand).first()
#         coin_obj=Coin.objects.filter(id=coin).first()
#         GameRoom

#         gameroom = GameRoom(
#             game=game_obj,
#             player=player_obj,

#         )



# class UpdateBeforeGameStartSerializer(serializers.ModelSerializer):
#     hand = serializers.CharField(allow_blank=True)
#     coin = serializers.CharField(allow_blank=True)
#     room_id = serializers.CharField(allow_blank=True)
#     game_id = serializers.CharField(allow_blank=True)
#     class Meta:
#         model = RoomManager
#         fields = ('game_id','room_id','hand','coin')

#     def validate(self,data):
#         game_id = data['game_id']
#         room_id = data['room_id']
#         hand = data['hand']
#         coin = data['coin']

#         if not game_id or game_id=='':
#             raise APIException({
#                 'message':'Game id is required',
#                 'success':'False',
#             })
#         if not room_id or room_id=='':
#             raise APIException({
#                 'message':'Room id is required',
#                 'success':'False',
#             })
#         if not hand or hand=='':
#             raise APIException({
#                 'message':'Hand value is required',
#                 'success':'False',
#             })
#         if not coin or coin=='':
#             raise APIException({
#                 'message':'Coin value is required',
#                 'success':'False',
#             })

#         return data

#     def create(self,validated_data):
#         game_id = validated_data['game_id']
#         room_id = validated_data['room_id']
#         hand = validated_data['hand']
#         coin = validated_data['coin']
#         ruser = self.context['ruser']

#         game = Game.objects.filter(id=game_id).first()
#         room = Room.objects.filter(socket_room_id=room_id).first()
#         hand = Hand.objects.filter(id=hand).first()
#         coin = Coin.objects.filter(id=coin).first()
        
#         if not room:
#             room=Room(
#                 game=game,
#                 socket_room_id=room_id,
#                 started_by=ruser,
#             )
#             room.save()
#         rm_obj = RoomManager.objects.filter(room=room,player=ruser).first()
#         if not rm_obj:
#             rm_obj = RoomManager(
#                 room=room,
#                 player=ruser,
#                 hand=hand,
#                 coin=coin,
#             )
#             rm_obj.save()
#         else:
#             rm_obj.hand = hand
#             rm_obj.coin = coin
#             rm_obj.save()
        
#         return validated_data