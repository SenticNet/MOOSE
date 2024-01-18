import os, argparse
import torch


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint_dir", type=str, default="./Checkpoints/chatgpt_50bkg_4itr_bkgnoter0_indirect1_onlyindirect2_close0_ban1_baseline0_survey1_bkgInspPasgSwap0_hypSuggestor1_hypEqlInsp_manualTitleSuggester_clearSplit_pastfdbkmodified_hypSuggestor", help="output directory")
    parser.add_argument("--research_background_id", type=int, default=5, help="id of the research background being used to generate research hypotheses")
    parser.add_argument("--hypothesis_id", type=int, default=0, help="id of those hypotheses generated from the research background")
    parser.add_argument("--hypothesis_refinement_round", type=int, default=0, help="refinement round of the hypothesis (present-feedback)")
    args = parser.parse_args()

    assert args.hypothesis_refinement_round >= 0 and args.hypothesis_refinement_round <= 3

    print("####### Parameters #######")
    print("checkpoint_dir:", args.checkpoint_dir)
    print("research_background_id:", args.research_background_id)
    print("hypothesis_id:", args.hypothesis_id)
    print("hypothesis_refinement_round:", args.hypothesis_refinement_round)

    data = torch.load(os.path.join(args.checkpoint_dir, "background_inspiration_hypotheses.pt"))
    research_background = data[2][args.research_background_id]
    research_inspirations = data[6][research_background][0]
    hypothesis = data[8][research_background][0][args.hypothesis_id][args.hypothesis_refinement_round]
    present_feedback = data[10][research_background][0][hypothesis]
    future_feedback = data[15][research_background][0][0]
    
    print("\n####### Research background #######\n", research_background)

    print("\n####### Research inspirations #######")
    for cur_insp_id, cur_insp in enumerate(research_inspirations):
        print("Inspiration {}: \t{}".format(cur_insp_id, cur_insp))

    print("\n####### Future-feedback (suggestions/explanations to be used for hypothesis generation) #######")
    print(future_feedback)

    print("\n####### Hypothesis #######\n", hypothesis)

    print("\n####### Present-feedback #######")
    print("#### Reality Feedback ####\n{}\n\n#### Novelty Feedback ####\n{}\n\n#### Clarity Feedback ####\n{}".format(present_feedback[0], present_feedback[1], present_feedback[2]))





if  __name__ == '__main__':
    main()