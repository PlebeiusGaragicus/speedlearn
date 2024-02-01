if __name__ == "__main__":
    # import dotenv
    # dotenv.load_dotenv()

    from backend.models import *
    from frontend.mainpage import mainpage

    # from src import logger
    # logger.setup_logging()
    # import logging
    # logging.getLogger("fsevents").setLevel(logging.WARNING)
    # logging.getLogger("matplotlib").setLevel(logging.WARNING)

    # import pdb; pdb.set_trace()

    import streamlit as st
    st.write("whatthefuck")
    mainpage()
