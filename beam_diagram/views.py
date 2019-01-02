from django.shortcuts import render, redirect, get_object_or_404
from .forms import beam_lengthForm, beam_supportForm, beam_pointLoadForm, beam_momentLoadForm, beam_distributedLoadForm
from .models import Beamlength, BeamSupport, PointLoad, MomentLoad, DistributedLoad
import numpy as np
from comments.models import Comment
from comments.forms import CommentForm
from django.contrib.contenttypes.models import ContentType

# Create your views here.


def new_beam(request):

    if request.method == 'POST':
        beam_lengthform = beam_lengthForm(request.POST)
        if beam_lengthform.is_valid():
            beam_length = beam_lengthform.cleaned_data['beam_length']
            beam = beam_lengthform.save(commit=False)
            beam.beam_length = beam_length
            beam.user = request.user
            beam = beam_lengthform.save()
            beamData = Beamlength.objects.all().order_by('-id')
            beamData = beamData[0]

            return redirect('new_beam:beam_diagram', beam_id=beamData.id)

    else:
        beam_lengthform = beam_lengthForm()
        context = {
            'beam_lengthform': beam_lengthform,
        }
        return render(request, 'new_beam.html', context)


def beam_diagram(request, beam_id):
    beamData = Beamlength.objects.get(id=beam_id)
    beamSupportData = BeamSupport.objects.filter(beamLength = beam_id).order_by('support_distance')
    beamPointLoadData = PointLoad.objects.filter(beamLength = beam_id).order_by('point_load_distance')
    beamMomentLoadData = MomentLoad.objects.filter(beamLength = beam_id).order_by('moment_load_distance')
    beamdistributedLoadData = DistributedLoad.objects.filter(beamLength = beam_id).order_by('start_distributed_load_location')

    if request.method == 'POST':
        beam_lengthform = beam_lengthForm(request.POST)
        beam_supportform = beam_supportForm(request.POST)
        beam_pointLoadform = beam_pointLoadForm(request.POST)
        beam_momentLoadform = beam_momentLoadForm(request.POST)
        beam_distributedLoadform = beam_distributedLoadForm(request.POST)

        beam_lengthform = beam_lengthForm(request.POST)
        if beam_lengthform.is_valid():
            beam_length = beam_lengthform.cleaned_data['beam_length']
            beam = beam_lengthform.save(commit=False)
            beam.beam_length = beam_length
            beam = beam_lengthform.save()
            beamData = Beamlength.objects.all().order_by('-id')
            beamData = beamData[0]

            return redirect('new_beam:beam_diagram', beam_id=beamData.id)

        if beam_lengthform.is_valid():
            beam_length = beam_lengthform.cleaned_data['beam_length']
            beam = beam_lengthform.save(commit=False)
            beam.beam_length = beam_length
            beam = beam_lengthform.save()

        if beam_supportform.is_valid():
            beam_support = beam_supportform.cleaned_data['support']
            support_distance = beam_supportform.cleaned_data['support_distance']
            beamSupport = beam_supportform.save(commit=False)
            beamSupport.beam_support = beam_support
            beamSupport.support_distance = support_distance
            beamSupport.save()

        if beam_pointLoadform.is_valid():
            beam_pointLoad = beam_pointLoadform.cleaned_data['point_load']
            pointLoad_distance = beam_pointLoadform.cleaned_data['point_load_distance']
            beamPointLoad = beam_pointLoadform.save(commit=False)
            beamPointLoad.point_load = beam_pointLoad
            beamPointLoad.point_load_distance = pointLoad_distance
            beamPointLoad.save()

        if beam_momentLoadform.is_valid():
            beam_momentLoad = beam_momentLoadform.cleaned_data['moment_load']
            momentLoad_distance = beam_momentLoadform.cleaned_data['moment_load_distance']
            beamMomentLoad = beam_momentLoadform.save(commit=False)
            beamMomentLoad.moment_load = beam_momentLoad
            beamMomentLoad.moment_load_distance = momentLoad_distance
            beamMomentLoad.save()

        if beam_distributedLoadform.is_valid():
            beam_distributedLoadform.save()


        return redirect('new_beam:beam_diagram', beam_id=beam_id)

    else:
        beam_lengthform = beam_lengthForm()
        beam_supportform = beam_supportForm(initial={'beamLength': beam_id})
        beam_pointLoadform = beam_pointLoadForm(initial={'beamLength': beam_id})
        beam_momentLoadform = beam_momentLoadForm(initial={'beamLength': beam_id})
        beam_distributedLoadform = beam_distributedLoadForm(initial={'beamLength': beam_id})

        context = {
            'beam_lengthform': beam_lengthform,
            'beam_supportform': beam_supportform,
            'beam_pointLoadform': beam_pointLoadform,
            'beam_momentLoadform': beam_momentLoadform,
            'beam_distributedLoadform': beam_distributedLoadform,


            'beamData': beamData,
            'beamSupportData': beamSupportData,
            'beamPointLoadData': beamPointLoadData,
            'beamMomentLoadData': beamMomentLoadData,
            'beamdistributedLoadData': beamdistributedLoadData,
            'beam_id': beam_id,
        }

        return render(request, 'beam_diagram.html', context)


def allUnique(data):
    seen = set()
    return not any(i in seen or seen.add(i) for i in data)


def beam_diagram_solve(request, beam_id):
    beamData = Beamlength.objects.get(id=beam_id)
    beamSupportData = BeamSupport.objects.filter(beamLength = beam_id).order_by('support_distance')
    beamPointLoadData = PointLoad.objects.filter(beamLength = beam_id).order_by('point_load_distance')
    beamMomentLoadData = MomentLoad.objects.filter(beamLength = beam_id).order_by('moment_load_distance')
    beamdistributedLoadData = DistributedLoad.objects.filter(beamLength = beam_id).order_by('start_distributed_load_location')


    # Determine distributed load type
    distributed_load_type = []
    for beamdistributedload in beamdistributedLoadData:
        distributed_load_type.append(beamdistributedload.start_distributed_load)
        distributed_load_type.append(beamdistributedload.end_distributed_load)

    print("distributed_load_type: ", distributed_load_type)


    # Determine condition of beam:
    beam_type = []
    support_distance = []
    for beam_support in beamSupportData:
        beam_type.append(beam_support.support)
        support_distance.append(beam_support.support_distance)

    simply_beam_condition = ['ROLLER SUPPORT', 'ROLLER SUPPORT']
    cantilever_beam_condition = ['FREE SUPPORT', 'FIXED SUPPORT']



    L = beamData.beam_length
    P = beamPointLoadData
    M  = beamMomentLoadData
    Q = beamdistributedLoadData

    if len(distributed_load_type) > 0:
        distributed_load_type = allUnique(distributed_load_type)
        # both distributed loads are equal
        if distributed_load_type == False:
            print("loads are equal")
            c1_q = []
            c2_q = []
            c3_q = []
            for c_qLoad in Q:
                e_d = c_qLoad.end_distributed_load_location - c_qLoad.start_distributed_load_location
                eplusd = c_qLoad.end_distributed_load_location + c_qLoad.start_distributed_load_location
                a = L - c_qLoad.end_distributed_load_location

                # for cantilivered beam will either use c1_q or c2_q
                c1_q.append(c_qLoad.start_distributed_load*(e_d)*(eplusd)*0.5)
                c2_q.append(c_qLoad.start_distributed_load*(e_d)*(e_d + 2*a)*0.5)
                c3_q.append(c_qLoad.start_distributed_load*(e_d))

            c1_m = sum(c1_q)
            c2_m = sum(c2_q)
            c3_m = sum(c3_q)



        else:
            print("loads are not equal")
    else:
        c1_m = 0
        c2_m = 0
        c3_m = 0


    c1_pb = []
    c2_pb = []
    c2_p = []

    for c_Pload in P:
        c1_pb.append(c_Pload.point_load*c_Pload.point_load_distance)
        c2_pb.append(c_Pload.point_load*(c_Pload.point_load_distance-L))
        c2_p.append(c_Pload.point_load)


    c_m = []
    for c_Mload in M:
        c_m.append(c_Mload.moment_load)

    c1_pb = sum(c1_pb)
    c2_pb = sum(c2_pb)
    c2_p = sum(c2_p)
    c_m = sum(c_m)


    c1 = c1_pb + c_m + c1_m
    c2 = c2_pb + c_m - c2_m



    simply_beam =  all(elem in beam_type for elem in simply_beam_condition)
    # If suport are a simply supported beam use this method
    if simply_beam:
        print("simply_beam: ", simply_beam)
        a = beamSupportData[0].support_distance
        f = beamSupportData[1].support_distance

        A = np.array([[a, -f], [(L-a), (L-f)]])
        B = np.array([[c1], [c2]])
        Reaction_Forces = (np.linalg.inv(A) @ B)
        Reaction_Forces = [item for sublist in Reaction_Forces for item in sublist]
        print("Reaction_Forces: ", Reaction_Forces)
        print("Support Distance: ", support_distance)

        P_list = []
        xP_list = []
        for P_region in P:
            P_list.append(P_region.point_load)
            xP_list.append(P_region.point_load_distance)

        M_list = []
        xM_list = []
        for M_region in M:
            M_list.append(M_region.moment_load)
            xM_list.append(M_region.moment_load_distance)

        q_list = []
        xq_list = []
        for q_region in Q:
            q_list.append(q_region.start_distributed_load)
            q_list.append(-q_region.end_distributed_load)
            xq_list.append(q_region.start_distributed_load_location)
            xq_list.append(q_region.end_distributed_load_location)


        xP_list = support_distance + xP_list

        print("xM_list: ", xM_list)
        x_new = xP_list + xM_list + xq_list
        print(x_new)

        P_list_tot = Reaction_Forces + P_list

        N_zeros_P = len(M_list + q_list)
        N_zeros_M = len(P_list_tot)
        N_zeros_Q = len(P_list_tot + M_list)
        P_list = P_list_tot + N_zeros_P*[0]
        M_list =  len(P_list_tot)*[0] + M_list + len(q_list)*[0]
        print("M_list: ", M_list)
        q_list =N_zeros_Q*[0] + q_list

        x_new1, P_list = zip(*sorted(zip(x_new, P_list)))
        x_new2, M_list = zip(*sorted(zip(x_new, M_list)))
        x_new3, q_list = zip(*sorted(zip(x_new, q_list)))
        print("x ", x_new1, "|\nP", P_list, "|\nM", M_list, "|\nq", q_list)


        V_shearQ = []
        V_ = []
        x_list = []
        x_range_forMo = []
        M_momentM = []
        for x in range(len(x_new1)):
            V = P_list[x]
            M = M_list[x]
            V_.append(V)
            V_shear_list = []
            M_momentM_list = []

            steps = 1
            if L <= 5:
                steps = 0.01
            elif L >= 5 and L <= 15:
                steps = 0.05
            elif L >= 15 and L <= 100:
                steps = 0.1

            x_new1List = list(x_new1)
            lastItem = x_new1[-1]
            x_new1List.append(lastItem)
            x_new1 = x_new1List

            if x+2 < len(x_new1):
                if x_new1[x] == x_new1[x+1]:
                    print("Region special: ", x_new1[x], "< x_2 <", x_new1[x+2])
                    x_range = np.arange(x_new1[x], x_new1[x+2], steps)
                    x_list.append(x_range)

                    for i_v in range(len(V_)):
                        V_shear = V_[i_v]*x_range**0 + q_list[i_v]*(x_range-x_new1[i_v])**1
                        V_shear_list.append(V_shear)

                    # for j_v in range(len(V_)):
                        Moment = V_[i_v]*(x_range-x_new1[i_v])**1 + (-M_list[i_v])
                        M_momentM_list.append(Moment)

                    V_shearQ.append(sum(V_shear_list))
                    M_momentM.append(sum(M_momentM_list))

                else:
                    print("Region: ", x_new1[x], "< x_2 <", x_new1[x+1])
                    x_range = np.arange(x_new1[x], x_new1[x+1], steps)
                    x_range_Mo = np.arange(x_new1[x], x_new1[x+1], steps)
                    x_list.append(x_range)

                    for i_v in range(len(V_)):
                        print("q_list: ", q_list)
                        print("x_new1[i_v]: ", x_new1[i_v])
                        # print("x_range: ", x_range)
                        V_shear = V_[i_v]*x_range**0 + q_list[i_v]*(x_range-x_new1[i_v])**1
                        V_shear_list.append(V_shear)

                        # print("M_list[i_v]: ", M_list, M_list[i_v])
                        print("V_: ", V_, V_[i_v]) #  (-M_list[i_v]) + q_list[i_v]*((x_range-x_new1[i_v])**2)*0.5
                        Moment = V_[i_v]*(x_range-x_new1[i_v])**1 + (-M_list[i_v]) + q_list[i_v]*((x_range-x_new1[i_v])**2)*0.5
                        M_momentM_list.append(Moment)

                    V_shearQ.append(sum(V_shear_list))
                    M_momentM.append(sum(M_momentM_list))



        print("##################################################")
        print("\n")
        x_list = np.concatenate(x_list).ravel().tolist()

        x_list = x_list
        V_shearQ = np.concatenate(V_shearQ).ravel().tolist()
        M_momentM = np.concatenate(M_momentM).ravel().tolist()

        # x_list, M_momentM = zip(*sorted(zip(x_list, M_momentM)))

        # x_list = np.asarray(x_list)
        # M_momentM = np.asarray(M_momentM)

        print(x_list)
        print(M_momentM)
        print("\n")







    cantilever_beam = all(elem in beam_type for elem in cantilever_beam_condition)
    # else if cantilivered beam
    if cantilever_beam:
        print("cantilever_beam: ", cantilever_beam)
        print("beam_type: ", beam_type)
        print("support_distance: ", support_distance)

        if support_distance[0] == float(0) and beam_type[0] == "FIXED SUPPORT":


            print("fixed on the left")
            A = - c2_p - c3_m
            M_A =  -1*(c1_pb + c_m + c1_m)
            Reaction_Forces_P = [A, 0]
            Reaction_Forces_M = [M_A]

            print("Reaction_Forces_M: ", A, M_A, Reaction_Forces_M)

            P_list = []
            xP_list = []
            for P_region in P:
                P_list.append(P_region.point_load)
                xP_list.append(P_region.point_load_distance)

            M_list = [M_A]
            xM_list = [0]
            for M_region in M:
                M_list.append(M_region.moment_load)
                xM_list.append(M_region.moment_load_distance)

            q_list = []
            xq_list = []
            for q_region in Q:
                q_list.append(q_region.start_distributed_load)
                q_list.append(-q_region.end_distributed_load)
                xq_list.append(q_region.start_distributed_load_location)
                xq_list.append(q_region.end_distributed_load_location)


            support_distance = support_distance
            xP_list = support_distance + xP_list

            print(xP_list)
            print(xM_list)

            x_new = xP_list + xM_list + xq_list
            print("x_new: ", x_new)

            P_list_tot = Reaction_Forces_P + P_list
            print("P_list_tot: ", P_list_tot)

            M_list_tot = M_list
            print("M_list_tot: ", M_list_tot)

            N_zeros_P = len(M_list_tot + q_list)
            N_zeros_M = len(P_list_tot + q_list)
            N_zeros_Q = len(P_list_tot + M_list_tot)
            P_list = P_list_tot + N_zeros_P*[0]

            print("P_list: ", P_list)

            M_list =  len(P_list_tot)*[0]  + M_list_tot + len(q_list)*[0]

            print("M_list: ", M_list)

            q_list =N_zeros_Q*[0] + q_list

            x_new1, P_list = zip(*sorted(zip(x_new, P_list)))
            x_new2, M_list = zip(*sorted(zip(x_new, M_list)))
            x_new3, q_list = zip(*sorted(zip(x_new, q_list)))
            print("x ", x_new1, "|\nP", P_list, "|\nM", M_list, "|\nq", q_list)
            x_new1 = x_new1[1:]
            P_list = P_list[1:]
            M_list = M_list[1:]
            q_list = q_list[1:]

            print("x_new1", x_new1)


            V_shearQ = []
            V_ = []
            x_list = []
            x_range_forMo = []
            M_momentM = []
            for x in range(len(x_new1)):
                V = P_list[x]
                M = M_list[x]
                V_.append(V)
                V_shear_list = []
                M_momentM_list = []

                steps = 1
                if L <= 5:
                    steps = 0.01
                elif L >= 5 and L <= 15:
                    steps = 0.05
                elif L >= 15 and L <= 100:
                    steps = 0.1

                x_new1List = list(x_new1)
                lastItem = x_new1[-1]
                x_new1List.append(lastItem)
                x_new1 = x_new1List

                if x+2 < len(x_new1):
                    if x_new1[x] == x_new1[x+1]:
                        print("Region special: ", x_new1[x], "< x_2 <", x_new1[x+2])
                        x_range = np.arange(x_new1[x], x_new1[x+2], steps)
                        x_list.append(x_range)

                    else:
                        print("Region: ", x_new1[x], "< x_2 <", x_new1[x+1])
                        x_range = np.arange(x_new1[x], x_new1[x+1], steps)
                        x_range_Mo = np.arange(x_new1[x], x_new1[x+1], steps)
                        x_list.append(x_range)

                    for i_v in range(len(V_)):
                        # print("x_range: ", x_range)
                        V_shear = V_[i_v]*x_range**0 + q_list[i_v]*(x_range-x_new1[i_v])**1
                        V_shear_list.append(V_shear)

                    # for j_v in range(len(V_)):
                        print("V_: ", V_)
                        print("M_list: ", M_list)
                        Moment = V_[i_v]*(x_range-x_new1[i_v])**1 + (-M_list[i_v]) + q_list[i_v]*((x_range-x_new1[i_v])**2)*0.5
                        print("Moment: ", Moment)
                        M_momentM_list.append(Moment)

                    V_shearQ.append(sum(V_shear_list))
                    M_momentM.append(sum(M_momentM_list))

        else:

            print("fixed on the right")
            A = - c2_p - c3_m
            M_A = - c2_pb - c_m + c2_m
            Reaction_Forces_P = [0, A]
            Reaction_Forces_M = [0, M_A]

            print("Reaction_Forces_P: ", A, M_A, Reaction_Forces_P)

            P_list = []
            xP_list = []
            for P_region in P:
                P_list.append(P_region.point_load)
                xP_list.append(P_region.point_load_distance)

            M_list = [M_A]
            xM_list = [0]
            for M_region in M:
                M_list.append(M_region.moment_load)
                xM_list.append(M_region.moment_load_distance)

            q_list = []
            xq_list = []
            for q_region in Q:
                q_list.append(q_region.start_distributed_load)
                q_list.append(-q_region.end_distributed_load)
                xq_list.append(q_region.start_distributed_load_location)
                xq_list.append(q_region.end_distributed_load_location)


            support_distance = support_distance
            xP_list = support_distance + xP_list

            print(xP_list)
            print(xM_list)

            x_new = xP_list + xM_list + xq_list
            print("x_new: ", x_new)

            P_list_tot = Reaction_Forces_P + P_list
            print("P_list_tot: ", P_list_tot)

            M_list_tot = M_list
            print("M_list_tot: ", M_list_tot)

            N_zeros_P = len(M_list_tot + q_list)
            N_zeros_M = len(P_list_tot + q_list)
            N_zeros_Q = len(P_list_tot + M_list_tot)
            P_list = P_list_tot + N_zeros_P*[0]

            print("P_list: ", P_list)

            M_list =  len(P_list_tot)*[0]  + M_list_tot + len(q_list)*[0]

            print("M_list: ", M_list)

            q_list =N_zeros_Q*[0] + q_list

            x_new1, P_list = zip(*sorted(zip(x_new, P_list)))
            x_new2, M_list = zip(*sorted(zip(x_new, M_list)))
            x_new3, q_list = zip(*sorted(zip(x_new, q_list)))
            print("x ", x_new1, "|\nP", P_list, "|\nM", M_list, "|\nq", q_list)
            x_new1 = x_new1[1:]
            P_list = P_list[1:]
            M_list = M_list[1:]
            q_list = q_list[1:]

            print("x_new1", x_new1)


            V_shearQ = []
            V_ = []
            x_list = []
            x_range_forMo = []
            M_momentM = []
            for x in range(len(x_new1)):
                V = P_list[x]
                M = M_list[x]
                V_.append(V)
                V_shear_list = []
                M_momentM_list = []

                steps = 1
                if L <= 5:
                    steps = 0.01
                elif L >= 5 and L <= 15:
                    steps = 0.05
                elif L >= 15 and L <= 100:
                    steps = 0.1

                x_new1List = list(x_new1)
                lastItem = x_new1[-1]
                x_new1List.append(lastItem)
                x_new1 = x_new1List

                if x+2 < len(x_new1):
                    if x_new1[x] == x_new1[x+1]:
                        print("Region special: ", x_new1[x], "< x_2 <", x_new1[x+2])
                        x_range = np.arange(x_new1[x], x_new1[x+2], steps)
                        x_list.append(x_range)

                    else:
                        print("Region: ", x_new1[x], "< x_2 <", x_new1[x+1])
                        x_range = np.arange(x_new1[x], x_new1[x+1], steps)
                        x_range_Mo = np.arange(x_new1[x], x_new1[x+1], steps)
                        x_list.append(x_range)

                    for i_v in range(len(V_)):
                        # print("x_range: ", x_range)
                        V_shear = V_[i_v]*x_range**0 + q_list[i_v]*(x_range-x_new1[i_v])**1
                        V_shear_list.append(V_shear)

                    # for j_v in range(len(V_)):
                        print("V_: ", V_)
                        print("M_list: ", M_list)
                        Moment = V_[i_v]*(x_range-x_new1[i_v])**1 + (-M_list[i_v]) + q_list[i_v]*((x_range-x_new1[i_v])**2)*0.5
                        # print("Moment: ", Moment)
                        M_momentM_list.append(Moment)

                    V_shearQ.append(sum(V_shear_list))
                    M_momentM.append(sum(M_momentM_list))



        print("##################################################")
        print("\n")
        x_list = np.concatenate(x_list).ravel().tolist()
        V_shearQ = np.concatenate(V_shearQ).ravel().tolist()
        M_momentM = np.concatenate(M_momentM).ravel().tolist()
        print("\n")


    beamData_post = get_object_or_404(Beamlength, id=beam_id)
    initial_data = {
        "content_type": beamData_post.get_content_type,
        "object_id": beamData_post.id,
    }



    form = CommentForm(request.POST or None, request.FILES or None, initial=initial_data)
    if form.is_valid() and request.user.is_authenticated:
        print("form is valid")
        # new_comment = form.save(commit=False)


        c_type = form.cleaned_data.get("content_type")
        content_type = ContentType.objects.get(model=c_type)
        obj_id = form.cleaned_data.get("object_id")
        content_data = form.cleaned_data.get("content")
        model_pic = form.cleaned_data.get("image")
        new_comment, created = Comment.objects.get_or_create(
            user = request.user,
            content_type=content_type,
            object_id = obj_id,
            content=content_data,
            image=model_pic,
        )

        if created:
            print("yeah")

        # new_comment = form.save()




    # content_type = ContentType.objects.get_for_model(BeamLength)
    # obj_id = beamData.id
    comments_list = Comment.objects.filter_by_product(beamData).order_by("-timestamp")
    print("comments_list: ", comments_list)


    context ={
        'beamData': beamData,
        'beamSupportData': beamSupportData,
        'beamPointLoadData': beamPointLoadData,
        'beamMomentLoadData': beamMomentLoadData,
        'beamdistributedLoadData': beamdistributedLoadData,
        'beam_id': beam_id,
        'x_list': x_list,
        'V_shearQ': V_shearQ,
        'M_momentM': M_momentM,
        'comments_list': comments_list,

        'comment_form': form,
    }


    return render(request, 'beam_diagram_solve.html', context)
