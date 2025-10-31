import time
from datetime import datetime

import requests
import streamlit as st

API_BASE_URL = "http://app:8000"


def get_api_info():
    try:
        response = requests.get(f"{API_BASE_URL}/api/info")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch API info: {e}")
        return None


def get_synonyms():
    try:
        start_time = time.time()
        response = requests.get(f"{API_BASE_URL}/api/synonyms")
        response.raise_for_status()
        elapsed_time = (time.time() - start_time) * 1000
        return response.json(), elapsed_time
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch synonyms: {e}")
        return None, 0


def main():
    st.set_page_config(
        page_title="Synonym System Dashboard", page_icon="📚", layout="wide"
    )

    st.title("Data Engine Synonym System")
    st.markdown("---")

    if "last_miss_time" not in st.session_state:
        st.session_state.last_miss_time = None

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("API Configuration")
        info = get_api_info()
        if info:
            info_col1, info_col2 = st.columns(2)
            with info_col1:
                st.metric("Cache Strategy", info.get("cache_strategy", "N/A").upper())
            with info_col2:
                st.metric(
                    "Cache TTL", f"{info.get('cache_ttl_seconds', 'N/A')} seconds"
                )

    with col2:
        if st.session_state.last_miss_time:
            ttl_seconds = 25
            elapsed = (datetime.now() - st.session_state.last_miss_time).total_seconds()
            remaining = max(0, ttl_seconds - elapsed)

            if remaining > 0:
                st.subheader("Cache Expiration Timer")
                st.metric("Time Until Expiry", f"{remaining:.1f}s")
                progress = remaining / ttl_seconds
                st.progress(progress)
            else:
                st.subheader("Cache Status")
                st.warning("Cache has expired")

    st.markdown("---")

    if st.button("Fetch Synonyms", type="primary", use_container_width=True):
        with st.spinner("Fetching data..."):
            data, elapsed = get_synonyms()

            if data:
                st.success(f"Request completed in {elapsed:.2f}ms")

                first_item = data[0] if data else {}
                cache_metadata = first_item.get("cache_metadata", {})
                from_cache = cache_metadata.get("from_cache", False)
                cache_info = cache_metadata.get("cache_info")

                metric_col1, metric_col2, metric_col3 = st.columns(3)

                with metric_col1:
                    cache_status = "HIT" if from_cache else "MISS"
                    status_color = "🟢" if from_cache else "🔴"
                    st.metric("Cache Status", f"{status_color} {cache_status}")

                with metric_col2:
                    if cache_info:
                        source = cache_info.get("cache_source", "N/A").upper()
                        st.metric("Cache Source", source)

                with metric_col3:
                    st.metric("Records Retrieved", len(data))

                if not from_cache:
                    st.session_state.last_miss_time = datetime.now()

                if cache_info and cache_info.get("cache_source") == "redis":
                    redis_host = cache_info.get("redis_host")
                    redis_port = cache_info.get("redis_port")
                    st.info(f"Redis: {redis_host}:{redis_port}")

                st.markdown("---")
                st.subheader("Synonym Records")

                search_term = st.text_input("Search by word", "")

                filtered_data = data
                if search_term:
                    filtered_data = [
                        item
                        for item in data
                        if search_term.lower() in item.get("word", "").lower()
                    ]

                st.dataframe(
                    [
                        {
                            "ID": item.get("word_id"),
                            "Word": item.get("word"),
                            "Synonyms": item.get("synonyms"),
                        }
                        for item in filtered_data
                    ],
                    use_container_width=True,
                    hide_index=True,
                )

    st.markdown("---")
    st.caption("Built with FastAPI, SQLAlchemy, Redis, and Streamlit")


if __name__ == "__main__":
    main()
